#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOTS = (
    "inbox",
    "topics",
    "reviews",
    "maps",
    "curriculum",
    "lessons",
    "assignments",
)
REQUIRED_FIELDS = ("id", "created", "status", "tags", "source", "visibility")
CONTENT_CONTRACTS = {
    "curriculum": {
        "required": ("kind", "track", "goal"),
        "values": {"kind": {"curriculum"}},
    },
    "lessons": {
        "required": (
            "kind",
            "track",
            "order",
            "estimated_minutes",
            "prerequisites",
        ),
        "values": {"kind": {"lesson"}},
    },
    "assignments": {
        "required": (
            "kind",
            "track",
            "lesson",
            "mode",
            "estimated_minutes",
        ),
        "values": {
            "kind": {"assignment"},
            "mode": {"guided", "faded", "independent", "transfer"},
        },
    },
}
ASSESSMENT_FIELDS = REQUIRED_FIELDS + (
    "kind",
    "track",
    "lesson",
    "estimated_minutes",
    "resource_policy",
    "objectives",
    "questions",
    "rubric",
    "answer_key",
    "misconception_routes",
    "reassessment",
    "review_schedule",
)
TEXT_SUFFIXES = {
    ".astro",
    ".css",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".yaml",
    ".yml",
}
IGNORED_DIRECTORIES = {".astro", ".git", "dist", "node_modules"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "assigned credential": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)"
        r"\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"
    ),
    "Supabase service-role key": re.compile(
        r"(?im)^\s*(?:SUPABASE_)?SERVICE_ROLE_KEY\s*=\s*[^\s#]{12,}\s*$"
    ),
}
LINK_PATTERN = re.compile(r"!?\[[^\]]*]\(([^)]+)\)")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def text_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and not IGNORED_DIRECTORIES.intersection(path.parts)
        and (path.suffix.lower() in TEXT_SUFFIXES or path.name.startswith(".env"))
    )


def content_notes() -> list[Path]:
    notes: list[Path] = []
    for root_name in CONTENT_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        notes.extend(
            path
            for path in root.rglob("*.md")
            if path.name.lower() != "readme.md"
        )
    return sorted(notes)


def assessment_files() -> list[Path]:
    root = ROOT / "assessments"
    if not root.exists():
        return []
    return sorted(root.rglob("*.json"))


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return {}, ["missing opening frontmatter delimiter"]

    try:
        end = lines.index("---", 1)
    except ValueError:
        return {}, ["missing closing frontmatter delimiter"]

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields, errors


def reject_duplicate_json_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key '{key}'")
        result[key] = value
    return result


def parse_json(path: Path) -> tuple[dict[str, object], list[str]]:
    import json

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=reject_duplicate_json_keys,
        )
    except (json.JSONDecodeError, ValueError) as error:
        return {}, [f"invalid JSON: {error}"]
    if not isinstance(value, dict):
        return {}, ["assessment root must be an object"]
    return value, []


def validate_date(value: str, path: str, errors: list[str]) -> None:
    try:
        date.fromisoformat(value)
    except ValueError:
        errors.append(f"{path}: created must use YYYY-MM-DD")


def validate_non_empty_string(
    value: object, field: str, path: str, errors: list[str]
) -> bool:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}: field '{field}' must be a non-empty string")
        return False
    return True


def validate_string_list(
    value: object,
    field: str,
    path: str,
    errors: list[str],
    *,
    allow_empty: bool = False,
) -> bool:
    if (
        not isinstance(value, list)
        or (not allow_empty and not value)
        or any(not isinstance(item, str) or not item.strip() for item in value)
    ):
        qualifier = (
            "a list of non-empty strings"
            if allow_empty
            else "a non-empty list of non-empty strings"
        )
        errors.append(f"{path}: field '{field}' must be {qualifier}")
        return False
    return True


def validate_positive_integer(
    value: object, field: str, path: str, errors: list[str]
) -> bool:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        errors.append(f"{path}: field '{field}' must be a positive integer")
        return False
    return True


def validate_object_list(
    value: object,
    field: str,
    required_fields: tuple[str, ...],
    path: str,
    errors: list[str],
) -> bool:
    if not isinstance(value, list) or not value:
        errors.append(f"{path}: field '{field}' must be a non-empty list")
        return False
    valid = True
    for index, item in enumerate(value):
        item_path = f"{path}: {field}[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_path} must be an object")
            valid = False
            continue
        for required in required_fields:
            if not validate_non_empty_string(
                item.get(required), required, item_path, errors
            ):
                valid = False
    return valid


def validate_notes(
    errors: list[str],
    ids: defaultdict[str, list[str]],
    lesson_ids: set[str],
    lesson_references: list[tuple[str, str]],
) -> None:

    for path in content_notes():
        rel = relative(path)
        fields, note_errors = parse_frontmatter(path)
        errors.extend(f"{rel}: {message}" for message in note_errors)

        for field in REQUIRED_FIELDS:
            if not fields.get(field):
                errors.append(f"{rel}: missing frontmatter field '{field}'")

        root_name = path.relative_to(ROOT).parts[0]
        contract = CONTENT_CONTRACTS.get(root_name)
        if contract:
            for field in contract["required"]:
                if not fields.get(field):
                    errors.append(f"{rel}: missing frontmatter field '{field}'")
            for field, allowed in contract["values"].items():
                if fields.get(field) not in allowed:
                    choices = ", ".join(sorted(allowed))
                    errors.append(f"{rel}: {field} must be one of: {choices}")

        if fields.get("id"):
            ids[fields["id"]].append(rel)
            if root_name == "lessons":
                lesson_ids.add(fields["id"])

        if root_name == "assignments" and fields.get("lesson"):
            lesson_references.append((rel, fields["lesson"]))

        created = fields.get("created")
        if created:
            validate_date(created, rel, errors)

        if fields.get("visibility") != "public":
            errors.append(f"{rel}: visibility must be public")

        tags = fields.get("tags")
        if tags and not (tags.startswith("[") and tags.endswith("]")):
            errors.append(f"{rel}: tags must use YAML list syntax")

        if root_name == "lessons":
            if fields.get("order") and not fields["order"].isdigit():
                errors.append(f"{rel}: order must be a positive integer")
            elif fields.get("order") == "0":
                errors.append(f"{rel}: order must be a positive integer")
            if fields.get("estimated_minutes") and (
                not fields["estimated_minutes"].isdigit()
                or fields["estimated_minutes"] == "0"
            ):
                errors.append(
                    f"{rel}: estimated_minutes must be a positive integer"
                )
            prerequisites = fields.get("prerequisites")
            if prerequisites and not (
                prerequisites.startswith("[") and prerequisites.endswith("]")
            ):
                errors.append(f"{rel}: prerequisites must use YAML list syntax")

        if root_name == "assignments" and fields.get("estimated_minutes") and (
            not fields["estimated_minutes"].isdigit()
            or fields["estimated_minutes"] == "0"
        ):
            errors.append(f"{rel}: estimated_minutes must be a positive integer")


def validate_assessments(
    errors: list[str],
    ids: defaultdict[str, list[str]],
    lesson_references: list[tuple[str, str]],
) -> None:
    for path in assessment_files():
        rel = relative(path)
        fields, parse_errors = parse_json(path)
        errors.extend(f"{rel}: {message}" for message in parse_errors)
        if parse_errors:
            continue

        for field in ASSESSMENT_FIELDS:
            if field not in fields:
                errors.append(f"{rel}: missing field '{field}'")

        for field in (
            "id",
            "created",
            "status",
            "source",
            "visibility",
            "kind",
            "track",
            "lesson",
        ):
            if field in fields:
                validate_non_empty_string(fields[field], field, rel, errors)

        assessment_id = fields.get("id")
        if isinstance(assessment_id, str) and assessment_id:
            ids[assessment_id].append(rel)
        lesson = fields.get("lesson")
        if isinstance(lesson, str) and lesson:
            lesson_references.append((rel, lesson))

        created = fields.get("created")
        if isinstance(created, str) and created:
            validate_date(created, rel, errors)

        if fields.get("visibility") != "public":
            errors.append(f"{rel}: visibility must be public")

        if fields.get("kind") != "assessment":
            errors.append(f"{rel}: kind must be assessment")

        if "tags" in fields:
            validate_string_list(
                fields["tags"], "tags", rel, errors, allow_empty=True
            )
        if "estimated_minutes" in fields:
            validate_positive_integer(
                fields["estimated_minutes"], "estimated_minutes", rel, errors
            )

        resource_policy = fields.get("resource_policy")
        if not isinstance(resource_policy, dict):
            errors.append(f"{rel}: field 'resource_policy' must be an object")
        else:
            validate_non_empty_string(
                resource_policy.get("mode"),
                "mode",
                f"{rel}: resource_policy",
                errors,
            )
            validate_string_list(
                resource_policy.get("allowed"),
                "allowed",
                f"{rel}: resource_policy",
                errors,
                allow_empty=True,
            )
            validate_string_list(
                resource_policy.get("prohibited"),
                "prohibited",
                f"{rel}: resource_policy",
                errors,
                allow_empty=True,
            )

        validate_object_list(
            fields.get("objectives"),
            "objectives",
            ("id", "statement"),
            rel,
            errors,
        )
        validate_object_list(
            fields.get("questions"),
            "questions",
            ("id", "type", "objective", "prompt"),
            rel,
            errors,
        )

        rubric = fields.get("rubric")
        if not isinstance(rubric, dict):
            errors.append(f"{rel}: field 'rubric' must be an object")
        else:
            validate_non_empty_string(
                rubric.get("passing_rule"),
                "passing_rule",
                f"{rel}: rubric",
                errors,
            )
            criteria = rubric.get("criteria")
            if validate_object_list(
                criteria,
                "criteria",
                ("id", "dimension", "meets"),
                f"{rel}: rubric",
                errors,
            ):
                for index, criterion in enumerate(criteria):
                    if not isinstance(criterion.get("critical"), bool):
                        errors.append(
                            f"{rel}: rubric: criteria[{index}]: field "
                            "'critical' must be a boolean"
                        )

        answer_key = fields.get("answer_key")
        if not isinstance(answer_key, dict) or not answer_key:
            errors.append(f"{rel}: field 'answer_key' must be a non-empty object")

        validate_object_list(
            fields.get("misconception_routes"),
            "misconception_routes",
            ("cause", "signal", "action"),
            rel,
            errors,
        )

        reassessment = fields.get("reassessment")
        if not isinstance(reassessment, dict):
            errors.append(f"{rel}: field 'reassessment' must be an object")
        else:
            validate_positive_integer(
                reassessment.get("earliest_delay_hours"),
                "earliest_delay_hours",
                f"{rel}: reassessment",
                errors,
            )
            variant = reassessment.get("variant")
            if not isinstance(variant, dict):
                errors.append(
                    f"{rel}: reassessment: field 'variant' must be an object"
                )
            else:
                for field in ("id", "prompt"):
                    validate_non_empty_string(
                        variant.get(field),
                        field,
                        f"{rel}: reassessment: variant",
                        errors,
                    )

        review_schedule = fields.get("review_schedule")
        if not isinstance(review_schedule, dict):
            errors.append(f"{rel}: field 'review_schedule' must be an object")
        else:
            days = review_schedule.get("after_provisional_days")
            if (
                not isinstance(days, list)
                or not days
                or any(
                    isinstance(day, bool)
                    or not isinstance(day, int)
                    or day <= 0
                    for day in days
                )
            ):
                errors.append(
                    f"{rel}: review_schedule: field "
                    "'after_provisional_days' must be a non-empty list of "
                    "positive integers"
                )
            validate_non_empty_string(
                review_schedule.get("retained_evidence"),
                "retained_evidence",
                f"{rel}: review_schedule",
                errors,
            )


def validate_assessment_extensions(errors: list[str]) -> None:
    root = ROOT / "assessments"
    if not root.exists():
        return
    for path in root.rglob("*"):
        if (
            path.is_file()
            and path.name.lower() != "readme.md"
            and path.suffix.lower() != ".json"
        ):
            errors.append(
                f"{relative(path)}: assessment definitions must use JSON"
            )


def validate_unique_ids(
    ids: defaultdict[str, list[str]], errors: list[str]
) -> None:
    for note_id, paths in ids.items():
        if len(paths) > 1:
            errors.append(f"duplicate id '{note_id}': {', '.join(paths)}")


def validate_lesson_references(
    lesson_ids: set[str],
    lesson_references: list[tuple[str, str]],
    errors: list[str],
) -> None:
    for path, lesson_id in lesson_references:
        if lesson_id not in lesson_ids:
            errors.append(
                f"{path}: referenced lesson '{lesson_id}' does not exist"
            )


def validate_secrets(files: list[Path], errors: list[str]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{relative(path)}: possible {label}")


def validate_links(files: list[Path], errors: list[str]) -> None:
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
                or "://" in target
            ):
                continue
            target = target.split("#", 1)[0]
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{relative(path)}: broken link '{target}'")


def main() -> int:
    errors: list[str] = []
    files = text_files()
    ids: defaultdict[str, list[str]] = defaultdict(list)
    lesson_ids: set[str] = set()
    lesson_references: list[tuple[str, str]] = []
    validate_notes(errors, ids, lesson_ids, lesson_references)
    validate_assessment_extensions(errors)
    validate_assessments(errors, ids, lesson_references)
    validate_unique_ids(ids, errors)
    validate_lesson_references(lesson_ids, lesson_references, errors)
    validate_secrets(files, errors)
    validate_links(files, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"validated {len(content_notes())} content notes, "
        f"{len(assessment_files())} assessments, "
        f"and {len(files)} text files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
