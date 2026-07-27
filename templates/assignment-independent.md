---
id: assignment-git-state-independent-001
created: 2026-07-27
status: ready
tags: [git, foundations, independent-practice]
source: lesson-git-working-tree-001
visibility: public
kind: assignment
track: git-cross-device
lesson: lesson-git-working-tree-001
mode: independent
estimated_minutes: 15
---

# Build a focused commit without guidance

## Objective

Select a coherent subset of several working-tree changes, verify the exact
staged content, commit it, and explain what remains without following a supplied
command sequence.

## Allowed resources

Git command help is allowed. The lesson, guided assignment, and saved command
sequences are not allowed.

## Scenario

In a disposable public practice repository, change `concept.md`, `example.md`,
and `scratch.md`. The next commit should contain the first two files and leave
`scratch.md` uncommitted.

## Expected artifact

Submit the commands used, the staged diff summary, the commit ID, the final
short status, and a brief explanation of why each file ended in its final
state.

## Constraints

- Do not use broad staging commands.
- Inspect the staged content before committing.
- Do not remove or overwrite `scratch.md`.
- Do not use force, reset, clean, or broad checkout commands.

## Rubric

| Criterion | Meets evidence |
| --- | --- |
| Explain | Correctly relates each file to working tree, staging area, and commit |
| Apply | The commit contains exactly `concept.md` and `example.md` |
| Diagnose | Final status for `scratch.md` is correctly interpreted |
| Safety | Only a disposable repository and non-destructive commands are used |

All criteria must meet the evidence without hints. Passing supports independent
practice evidence; retained mastery still requires delayed retrieval or
transfer.

## Corrective routes

- If every file is staged, repeat with different filenames and name each
  intended path explicitly.
- If the staged diff is skipped, practice the sequence “inspect, select, verify,
  commit” with a new scenario.
- If the artifact is correct but the explanation is weak, predict each status
  transition before repeating one varied task.
