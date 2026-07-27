# Curriculum

Curriculum files define why and in what dependency order Miles studies a
subject. They are navigation contracts, not concept explanations. Keep the
durable explanation of a concept in `topics/` and refer to it from a track.

## One track per file

A track should define:

- one practical goal and the observable final capability;
- the intended learner and any assumed starting knowledge;
- an acyclic prerequisite graph;
- an ordered path through the graph;
- evidence required to unlock each concept;
- the lesson, assignment, and assessment IDs used for that evidence;
- one final transfer task in a context not copied from the lessons.

Use a stable filename such as `git-cross-device.md`. A track may change its
recommended order, but published IDs and evidence references stay stable.

## Required metadata

Curriculum files use the repository's common public frontmatter (`id`,
`created`, `status`, `tags`, `source`, and `visibility`) plus:

```yaml
kind: curriculum
track: git-cross-device
goal: synchronize-git-work-safely-across-devices
```

Use `status: draft`, `active`, or `retired`. `visibility` is always `public`.
The body should contain Goal, Starting point, Prerequisite graph, Ordered path,
Advancement evidence, Final transfer task, and Related canonical topics.

## Example dependency path

```text
working tree
  -> staging and commits
  -> local and remote branches
  -> fetch and rebase
  -> conflict resolution
  -> safe cross-device synchronization
```

For `working tree`, advancement evidence could require Miles to explain the
three file states, classify a real `git status` output, and complete the
referenced independent assignment. The track records those requirements; the
lesson teaches them and the assessment judges them.

## Boundaries

- Do not duplicate explanations from `topics/`.
- Do not mark a node complete because its lesson or test file exists.
- Do not place attempts, scores, hints used, or due dates in the track. Those
  belong in a progress store; only the current summary belongs in
  `maps/progress.md`.
- Do not include private work examples. Generalize scenarios so every track is
  safe in this public repository.
