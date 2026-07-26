#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOTS = ("inbox", "topics", "reviews", "maps")
REQUIRED_FIELDS = ("id", "created", "status", "tags", "source", "visibility")
TEXT_SUFFIXES = {".md", ".py", ".sh", ".yml", ".yaml", ".json", ".toml"}
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "assigned credential": re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret)"
        r"\s*[:=]\s*['\"][^'\"\s]{12,}['\"]"
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
        and ".git" not in path.parts
        and path.suffix.lower() in TEXT_SUFFIXES
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


def validate_notes(errors: list[str]) -> None:
    ids: defaultdict[str, list[str]] = defaultdict(list)

    for path in content_notes():
        rel = relative(path)
        fields, note_errors = parse_frontmatter(path)
        errors.extend(f"{rel}: {message}" for message in note_errors)

        for field in REQUIRED_FIELDS:
            if not fields.get(field):
                errors.append(f"{rel}: missing frontmatter field '{field}'")

        if fields.get("id"):
            ids[fields["id"]].append(rel)

        created = fields.get("created")
        if created:
            try:
                date.fromisoformat(created)
            except ValueError:
                errors.append(f"{rel}: created must use YYYY-MM-DD")

        if fields.get("visibility") != "public":
            errors.append(f"{rel}: visibility must be public")

    for note_id, paths in ids.items():
        if len(paths) > 1:
            errors.append(f"duplicate id '{note_id}': {', '.join(paths)}")


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
    validate_notes(errors)
    validate_secrets(files, errors)
    validate_links(files, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"validated {len(content_notes())} content notes "
        f"and {len(files)} text files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
