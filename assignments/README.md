# Assignments

Assignments produce practice evidence for one named objective. Keep each file
focused on one mode so support can fade without silently changing the task.

## Practice modes

| Mode | Prompt support | Evidence expected |
| --- | --- | --- |
| `guided` | Explicit steps and bounded hints | Miles follows the process and explains decisions |
| `faded` | Some steps removed | Miles supplies the missing decisions |
| `independent` | Goal and constraints only | Miles produces a complete artifact |
| `transfer` | A different context | Miles chooses and applies the concept without cues |

## Required contract

Each assignment uses the common public frontmatter and adds:

```yaml
kind: assignment
track: git-cross-device
lesson: lesson-git-working-tree-001
mode: guided
estimated_minutes: 15
```

Its body states the observable objective, allowed resources, scenario or input,
expected artifact, constraints, submission instructions, rubric, hints, and
the corrective route for each likely failure.

Hints reveal less than the full solution and are ordered from least to most
supportive. An attempt records which hint was used; the assignment file remains
unchanged. A correct guided response is not independent evidence.

## Attempt boundary

Do not commit detailed attempts, raw answers, scores, or UI events into an
assignment file. Store them in the authenticated progress store. A public,
agent-readable checkpoint may summarize the artifact path, rubric evidence,
and next action in `maps/progress.md` only when the summary itself is safe to
publish.

Use `templates/assignment.md` as the guided example and
`templates/assignment-independent.md` as the matching independent example.
Create separate files for faded and transfer variants, each with a new stable
ID and the same objective where appropriate.
