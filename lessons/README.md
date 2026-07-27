# Lessons

Lessons are bounded teaching units. A lesson turns one or a few canonical
concepts into an explanation, worked example, recall check, and explicit route
to practice. It does not own the canonical concept definition or learner
progress.

## Required contract

Each lesson file uses the common public frontmatter and adds:

```yaml
kind: lesson
track: git-cross-device
order: 1
estimated_minutes: 25
prerequisites: []
```

The body contains, in order:

1. observable learning objectives;
2. prerequisite check;
3. plain-language explanation linked to canonical topics;
4. one worked example that exposes the reasoning;
5. one common misconception and a counterexample;
6. a short recall check whose answer is not shown before retrieval;
7. IDs or paths for guided and independent assignments;
8. an assessment reference;
9. the next concept.

Split a lesson when its objectives cannot be practiced and assessed in one
session. Keep answers to the recall check in a collapsible section or a
separate answer block that the Web UI can hide until Miles submits.

## State boundary

Opening a lesson may support `learning`; it is not evidence for `practiced`,
`provisional`, or `retained`. The UI records detailed events and attempts in a
progress store. Agents summarize only verified evidence in
`maps/progress.md`.

Use `templates/lesson.md` as the complete foundation-level example. When
adapting it, preserve the sequence from objective through next concept and
replace all sample content with publishable material.
