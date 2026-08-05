---
name: continue-study
description: Resume and guide Miles's public cross-device learning from repository evidence. Use when Miles asks to continue or start studying, explain a concept from foundations, create a curriculum, give guided or independent assignments, administer or grade an assessment, correct misconceptions, schedule review, record learning progress, or prepare a Web UI for the mingi-miles-study repository.
---

# Continue Study

Use the repository as the durable learning context. Carry Miles from the exact
stopping point through one useful learning step, then leave enough evidence for
another device or agent to continue.

## Local adaptations (filled in per installed copy only, never in canonical)

This file at `.agents/skills/continue-study/` inside the repository is
canonical. Every installed copy — on any device, for any agent — adds its own
version of this section directly below this heading, and nowhere else in the
file:

- Local clone path
- Remote source of truth (the repo URL, restated for convenience)
- `Synced at commit: <hash> (<date>)` — the canonical commit at path
  `.agents/skills/continue-study/` this installed copy last adopted

## Stay current with canonical

Before anything else in a session that uses this skill:

1. Run `git -C <local clone path> log -1 --format=%H -- .agents/skills/continue-study/`
   and compare the result to this file's own `Synced at commit` value above.
2. If they match, proceed normally.
3. If they differ, resync first: open the canonical files at that path in the
   clone, diff them against this installed copy, adopt every change except the
   "Local adaptations" section itself, then update `Synced at commit` to the
   new hash and date.
4. Mention what changed, briefly, at the point it's relevant in this session's
   report. This step is what makes a skill change reach every device and agent
   without Miles telling each one by hand.

## Start safely

1. Run the sync check above, then locate the `mingi-miles-study` clone and
   read its `AGENTS.md`.
2. Run `scripts/learn status` before writing.
3. Report existing changes and preserve them.
4. Read `maps/progress.md` when present, then verify it against recent relevant
   inbox, lesson, topic, assignment, assessment, and review files.
5. Separate verified repository state from inference.
6. Pull or sync only when the working tree is safe and current remote state is
   needed.

Never infer completed learning from a plan, a generated lesson, or an unanswered
assignment.

## Route the request

| Miles's intent | Action |
| --- | --- |
| Continue or resume | Orient from the latest checkpoint and begin its next action |
| Start a subject | Build a foundation-first prerequisite path before teaching |
| Explain a concept | Teach one bounded concept with a worked example |
| Give practice | Choose guided or independent work based on current evidence |
| Test understanding | Administer a closed-resource assessment with a stated rubric |
| Review an answer | Grade against the rubric and cite answer evidence |
| Fix a mistake | Diagnose the misconception and give a different corrective activity |
| Finish a session | Write the learning log and exact checkpoint, then sync |
| Build a learning UI | Read `references/web-ui.md` and use the bundled Astro template |

Read `references/learning-model.md` before creating curricula, lessons,
assignments, assessments, mastery decisions, or progress checkpoints.

## Run one learning cycle

### 1. Orient

State:

- current subject and track;
- verified mastery state;
- recent activity;
- unresolved questions;
- exact stopping point;
- one smallest useful next action;
- repository paths supporting the summary.

If no checkpoint exists, say so and reconstruct only what the files support.

### 2. Select the next concept

Choose the lowest unmet prerequisite that advances the active goal. Keep the
unit small enough to explain and practice in one session. Do not skip a
prerequisite merely to make visible progress.

For a new track, record:

- goal and intended capability;
- ordered concepts and dependencies;
- evidence required to advance;
- final transfer task.

### 3. Teach

Present the learning unit in this order:

1. what Miles should be able to do;
2. prerequisites;
3. plain-language explanation;
4. one concrete worked example with reasoning;
5. common misconception;
6. a short recall check without showing the answer.

Do not confuse recognition with understanding. Ask Miles to explain or produce
an answer before revealing the solution.

### 4. Assign practice

Use progressive independence:

1. guided task with explicit steps or hints;
2. partially guided variant when needed;
3. independent task with no solution path exposed;
4. transfer task in a different context.

Keep each task tied to a named learning objective. Do not add unrelated
difficulty.

### 5. Assess

State whether notes and tools are allowed before beginning. Prefer constructed
responses, code, diagrams, or concrete artifacts over recognition-only
questions.

Grade each objective against its rubric. Record:

- submitted answer or artifact reference;
- criterion-level evidence;
- result per criterion;
- confidence and any grading uncertainty;
- next corrective or review action.

Do not mark a concept retained from an immediate test. Use the state rules in
`references/learning-model.md`.

### 6. Correct

Classify the failure before teaching again:

- missing prerequisite;
- inaccurate mental model;
- procedural error;
- weak retrieval;
- transfer failure;
- ambiguous question or rubric.

Give targeted feedback, a shorter alternate explanation, and a new variant
task. Do not repeat the same failed question as proof of learning.

### 7. Review

Schedule a delayed recall after provisional success. At review time, ask for
retrieval before showing prior notes. Advance to retained only when the delayed
evidence meets the rubric.

### 8. Checkpoint and sync

At a meaningful stopping point:

1. create a chronological public learning log when new learning occurred;
2. update `maps/progress.md` with current understanding, open questions, exact
   stopping point, next action, and related paths;
3. validate the repository;
4. run `scripts/learn sync`;
5. verify the pushed commit before claiming another device can resume.

The checkpoint must be useful without access to the current conversation.

## Build or adapt the Web UI

Read `references/web-ui.md` for architecture and deployment guidance. Copy
`assets/web-ui-template/` as a starting point rather than rewriting the same
Astro scaffold.

Preserve this separation:

- Git repository: public curriculum, lessons, assignments, assessments,
  rubrics, and agent-readable checkpoints.
- Progress store: attempts, scores, due dates, and detailed UI events.
- Generated checkpoint: concise repository summary derived from verified
  progress, never a second independent source of truth.

The bundled template may use browser-local progress for development. Do not
describe it as cross-device synchronization. Use authenticated storage with
per-user authorization before making that claim.

## Public boundary

Write only material safe for a public repository. Reject credentials, private
keys, customer source material, private message transcripts, internal network
locations, account details, and non-public attachments.

Generalize work experience before recording it. Preserve public attribution.
When publication safety is unclear, stop and ask Miles before writing or
pushing.

## Finish with evidence

Report:

- what Miles studied or what capability was added;
- changed learning state;
- assignment or assessment evidence;
- checkpoint and commit path;
- validation performed;
- unresolved questions and exact next action.

Do not report mastery, synchronization, build success, or deployment without
direct evidence.
