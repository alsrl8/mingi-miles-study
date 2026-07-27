---
id: lesson-git-working-tree-001
created: 2026-07-27
status: ready
tags: [git, foundations, cross-device]
source: public-git-documentation
visibility: public
kind: lesson
track: git-cross-device
order: 1
estimated_minutes: 25
prerequisites: []
---

# Working tree, staging area, and commit

## Learning objectives

After this lesson, Miles can:

- explain the difference between a working-tree change, a staged change, and a
  committed snapshot;
- read a short `git status` result and identify the next safe command;
- predict which content a commit will include.

## Prerequisite check

This is the first unit in the track. Miles only needs to know that a Git
repository tracks versions of files. If “repository” and “ordinary folder”
still feel identical, first compare a folder with and without a `.git`
directory and explain which one retains commit history.

## Concept in plain language

Think of a change as moving through three places.

The working tree is the version currently visible and editable on the device.
The staging area is a proposed list of exact changes for the next snapshot. A
commit is the saved snapshot plus its history metadata. Editing a file does not
stage it, and staging it does not commit it.

This separation lets one working tree contain several edits while a commit
includes only the coherent subset selected for that snapshot.

## Worked example

Suppose `notes.md` and `README.md` are both edited, but only the learning note
belongs in the next commit.

1. `git status --short` shows both files with ` M`, meaning they changed in the
   working tree and are not staged.
2. `git add notes.md` copies the current `notes.md` change into the staging
   area.
3. A second `git status --short` shows `M ` for `notes.md` and ` M` for
   `README.md`. The first column describes the staged state; the second
   describes the working tree.
4. `git commit -m "Record Git state lesson"` saves the staged `notes.md`
   content. The unstaged `README.md` edit remains in the working tree.

The reasoning is “inspect, select, verify, commit,” not “commit every changed
file.”

## Common misconception

“`git add` saves the change permanently” is inaccurate. If the repository is
deleted before a commit is created and copied elsewhere, the staging area does
not provide a portable history checkpoint. A commit is the durable repository
snapshot; a push is what makes that commit available from the remote.

## Recall check

Without running Git, explain which file a commit includes after this sequence:

```text
edit a.md
edit b.md
git add a.md
edit a.md again
git commit
```

State what remains in the working tree after the commit.

<details>
<summary>Reveal after answering</summary>

The commit contains the version of `a.md` captured at `git add` time. The later
edit to `a.md` and the edit to `b.md` remain unstaged in the working tree.

</details>

## Practice route

- Guided assignment: `assignment-git-state-guided-001`
- Independent assignment: `assignment-git-state-independent-001`
- Assessment: `assessment-git-state-001`

Use the guided task first when there is no prior evidence. Move to independent
practice only after Miles can explain why each state changes.

## Next concept

Continue to “local commits and remote branches” after the independent artifact
meets its rubric. Do not advance merely because this page was read.
