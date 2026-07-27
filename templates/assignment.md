---
id: assignment-git-state-guided-001
created: 2026-07-27
status: ready
tags: [git, foundations, guided-practice]
source: lesson-git-working-tree-001
visibility: public
kind: assignment
track: git-cross-device
lesson: lesson-git-working-tree-001
mode: guided
estimated_minutes: 15
---

# Build one focused commit

## Objective

Classify working-tree and staging-area state, then create a commit containing
only the intended file while explaining each decision.

## Allowed resources

The lesson and local Git documentation are allowed. Do not copy a command
sequence without explaining what each command verifies or changes.

## Scenario

In a disposable practice repository, create `concept.md` and `scratch.md`.
Only `concept.md` belongs in the learning-history commit. `scratch.md` must
remain uncommitted.

## Steps

1. Create both files with one sentence of harmless sample text.
2. Inspect their state with `git status --short` and label each status column.
3. Stage only `concept.md`.
4. Inspect the state again and predict the exact commit contents.
5. Commit with a message that describes the learning artifact.
6. Inspect the final state and explain why `scratch.md` remains.

## Expected artifact

Submit the three `git status --short` outputs, the commit ID, and a
three-sentence explanation covering working tree, staging area, and commit.
Use only disposable public sample content.

## Constraints

- Do not use `git add .` or `git add -A`.
- Do not delete or stage `scratch.md`.
- Do not use force, reset, clean, or broad checkout commands.
- Perform the task only in a disposable practice repository.

## Rubric

| Criterion | Meets evidence |
| --- | --- |
| Explain | Correctly distinguishes all three states in the learner's own words |
| Apply | The commit contains `concept.md` and excludes `scratch.md` |
| Diagnose | Final status is interpreted correctly rather than treated as an error |
| Safety | No destructive command or private content is used |

All four criteria must meet the evidence. Safety and Apply are critical and
cannot be offset by the explanation.

## Hints

Use at most one hint at a time and record which one was used.

1. The staging command can name one path rather than the whole repository.
2. In short status, the left column describes the index and the right column
   describes the working tree.
3. Compare `git diff --cached` with `git diff` before committing.

## Corrective routes

- If both files are committed, repeat a new variant using three files and name
  only the intended path when staging.
- If the state columns are reversed, annotate one fresh status output as
  “index, working tree” before retrying.
- If the commands work but the explanation is weak, predict the next status
  output before executing each command in a new practice repository.

Passing this guided task supports `practiced` evidence with help. It does not
prove independent application or delayed retention.
