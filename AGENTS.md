# Agent Instructions

## Purpose

This repository is Miles's public, cross-device learning source of truth. Help
capture observations, distill reusable knowledge, connect related topics, and
prepare review questions.

## Public boundary

- Store only material that is safe to publish.
- Never add credentials, tokens, private keys, customer source material,
  private message transcripts, internal network locations, or non-public
  attachments.
- Generalize work experience into reusable principles before recording it.
- Preserve attribution when a public source informed a note.
- Stop and ask Miles when the publication status of material is unclear.

## Content model

- `inbox/`: one new file per observation; do not combine unrelated captures.
- `topics/`: durable explanations that can be understood without chat history.
- `reviews/questions/`: retrieval questions with answers in the same document.
- `reviews/weekly/`: dated reflection on what changed in Miles's understanding.
- `maps/`: indexes that connect topics without duplicating their content.

Content notes other than directory `README.md` files must begin with frontmatter
containing `id`, `created`, `status`, `tags`, `source`, and `visibility`.
Visibility must be `public`.

## Git workflow

- Treat the GitHub repository as the source of truth.
- Run `scripts/learn sync` before switching devices.
- Create inbox notes as new files to minimize merge conflicts.
- Distill or substantially revise topics on a branch and merge through a pull
  request.
- Never rebuild or delete the repository from external source directories.
- Preserve unrelated uncommitted work and never force-push.

## Quality

- Prefer concise explanations, concrete examples, and links between related
  notes.
- Separate verified facts from personal conclusions.
- Do not leave placeholder sections, TODOs, or empty references.
- Run `python3 scripts/validate.py`, `bash tests/test_learn.sh`, and
  `git diff --check` before pushing structural or script changes.
