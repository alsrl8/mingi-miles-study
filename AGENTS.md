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
- `curriculum/`: goals, prerequisite graphs, learning order, and advancement
  evidence; link to canonical topics instead of copying explanations.
- `lessons/`: bounded teaching units with objectives, explanation, worked
  example, misconception, recall check, and practice routes.
- `assignments/`: guided, faded, independent, or transfer practice definitions;
  keep one support mode per file.
- `assessments/`: questions, criterion-level rubrics, variants, and corrective
  routes; keep learner attempts out of the definition.
- `reviews/questions/`: retrieval questions with answers in the same document.
- `reviews/weekly/`: dated reflection on what changed in Miles's understanding.
- `maps/`: indexes that connect topics without duplicating their content;
  `maps/progress.md` is the current agent-readable checkpoint.
- Progress store: detailed attempts, answers, scores, hints, due dates, and UI
  events. It is not a second canonical copy of public learning content.

Markdown content notes other than directory `README.md` files must begin with
frontmatter containing `id`, `created`, `status`, `tags`, `source`, and
`visibility`. Assessment definitions use JSON instead; those fields are
required as top-level JSON properties. Visibility must be `public`.

Read `.agents/skills/continue-study/SKILL.md` and its
`references/learning-model.md` before creating or grading a curriculum, lesson,
assignment, assessment, mastery decision, or progress checkpoint. Use the
complete examples in `templates/` as structural starting points.

## Learning evidence

- Use `locked`, `learning`, `practiced`, `provisional`, `review_due`, and
  `retained` as the mastery progression.
- Never infer progress from a file's existence, a plan, or an unanswered
  exercise.
- Grade explain, apply, diagnose, and transfer dimensions against stated rubric
  evidence; do not average away a failed critical criterion.
- Immediate assessment can support `provisional`, not `retained`. Require a
  delayed closed-resource retrieval or transfer result for `retained`.
- Classify an error before correction and use a different reassessment variant.
- Update `maps/progress.md` with verified activity, current interpretation,
  unresolved questions, the exact stopping point, one next action, and
  supporting repository paths.
- Do not claim cross-device continuity until the checkpoint commit is pushed
  and verified. Browser-local progress is development-only and single-device.

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
