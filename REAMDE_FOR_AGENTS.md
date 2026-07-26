# Guide for Agents

## What this repository is

`mingi-miles-study` is Miles's, also known as Mingi's, public cross-device
learning source of truth. Its primary purpose is to share learning logs,
progress, current context, and next steps so Miles can continue studying from
any device or agent without reconstructing the previous session.

Agents use it to capture what Miles studied, preserve where he stopped, state
what remains unresolved, resume the next session, turn observations into durable
explanations, connect related knowledge, and prepare material for later recall.

The repository is not a one-way mirror assembled from another machine. GitHub is
the canonical copy, and every device may contribute through normal Git commits
and pull requests.

Read `AGENTS.md` before changing content or implementation. Read `README.md` for
the human-facing workflow.

## Skillset

The current implementation exposes the following capabilities through
`scripts/learn` and `scripts/validate.py`. An agent may wrap these commands as
local skills or implement equivalent skills in another runtime.

| Recommended skill | Current command | Responsibility |
| --- | --- | --- |
| `study-orient` | repository conventions | Reconstruct the current learning subject, recent progress, unresolved questions, and next action |
| `study-status` | `scripts/learn status` | Show the active branch, local changes, latest commit, and origin |
| `study-capture` | `scripts/learn capture` | Create one public inbox note with a collision-resistant ID |
| `study-progress` | repository conventions | Record what was studied, current understanding, stopping point, and next step |
| `study-sync` | `scripts/learn sync` | Receive remote changes, validate, commit local work, and push safely |
| `study-issue` | `scripts/learn issue` | Capture a public observation through a GitHub Issue when no clone is available |
| `study-distill` | `scripts/learn distill` | Convert a committed inbox note into a topic on a dedicated branch |
| `study-validate` | `scripts/validate.py` | Enforce metadata, unique IDs, valid links, and basic secret checks |
| `study-review` | repository conventions | Create retrieval questions, weekly reviews, and learning maps |

These names describe capabilities, not a required skill framework. Codex,
Claude, a shell agent, or another automation system may use different names as
long as it preserves the contracts below.

## Continuity contract

Every agent implementation should make it possible to answer these questions
from the repository alone:

1. What is Miles studying now?
2. What did he study most recently?
3. What does he currently understand?
4. Which questions or uncertainties remain?
5. Where did the previous session stop?
6. What is the smallest useful next action?
7. Which files contain the evidence and durable explanation?

The latest progress record is a handoff, not a general summary. It should be
short enough to read at the start of every session and precise enough that a
different agent can continue without hidden chat context.

## Shared content contract

Content belongs in one of these areas:

- `inbox/`: one observation per file, created without modifying another note.
- `topics/`: reusable explanations that make sense without conversation history.
- `reviews/questions/`: questions and answers for retrieval practice.
- `reviews/weekly/`: dated reflection on changed understanding.
- `maps/`: links between canonical topic notes.

Use `maps/progress.md` as the current learning checkpoint when an agent adds a
progress capability. Keep only the current state there; preserve chronological
learning events as separate notes in `inbox/` and dated reviews.

Every content note other than a directory `README.md` begins with:

```yaml
---
id: globally-unique-note-id
created: 2026-07-27
status: inbox
tags: []
source: direct-experience
visibility: public
---
```

An equivalent implementation must preserve these fields:

- `id`: unique across the repository and stable after creation.
- `created`: local calendar date in `YYYY-MM-DD`.
- `status`: the note's stage, such as `inbox` or `distilled`.
- `tags`: a list, empty when classification is not yet useful.
- `source`: a public reference or a non-sensitive provenance description.
- `visibility`: always `public`.

## Skill contracts

### `study-orient`

Use this first when Miles wants to continue studying from another device or
agent.

Inputs:

- Repository working directory.
- Optional subject named by Miles.

Outputs:

- Current learning subject.
- Most recent relevant learning logs.
- Current understanding and progress.
- Unresolved questions.
- Exact stopping point.
- One concrete next action.
- Paths to the relevant notes.

Rules:

- Pull or sync only when Miles asked for current remote state and the working
  tree is safe to update.
- Read `maps/progress.md` when present, then verify it against recent inbox,
  topic, and review notes.
- Separate repository facts from the agent's inference.
- Do not invent progress when no checkpoint exists.
- Do not start a new subject merely because the previous one looks complete.

### `study-status`

Use this first when an agent enters an existing clone.

Inputs:

- Repository working directory.

Outputs:

- Active branch.
- Working-tree changes.
- Latest local commit.
- Configured origin.

Rules:

- It is read-only.
- It does not pull, commit, switch branches, or modify files.
- The agent must report existing changes before editing them.

### `study-capture`

Use this for a new observation that is not yet a durable topic.

Inputs:

- Required title.
- Optional body; when omitted, the title is also the body.

Outputs:

- One new Markdown file below `inbox/YYYY/MM/`.
- The repository-relative path of that file.

Rules:

- Generate a new file instead of appending to a shared daily file.
- Include a UTC timestamp and device-specific component in the ID.
- Slugify the title for the filename, with a deterministic fallback when the
  title contains no ASCII characters.
- Never overwrite an existing path.
- Validate the repository after writing.

The current command is:

```bash
scripts/learn capture "Title" "What Miles learned"
```

### `study-progress`

Use this near the end of a study session or whenever Miles changes devices.

Inputs:

- Current subject.
- What Miles studied during the session.
- What Miles can now explain or apply.
- Remaining questions or blockers.
- Exact stopping point.
- Recommended next action.
- Paths to supporting inbox or topic notes.

Outputs:

- An updated `maps/progress.md`.
- A chronological learning log when the session produced new learning.

The progress file should contain:

```yaml
---
updated: 2026-07-27
subject: current-learning-subject
status: active
visibility: public
---
```

Its body should state `Recent activity`, `Current understanding`, `Open
questions`, `Stopped at`, `Next action`, and `Related notes` with concrete
content. Do not create empty sections.

Rules:

- Update progress from verified session facts, not an optimistic plan.
- Keep the next action small enough to begin immediately on another device.
- Link to chronological notes instead of copying their full content.
- Do not erase unresolved questions merely because the session is ending.
- Validate and sync the checkpoint before claiming the handoff is available
  elsewhere.

### `study-sync`

Use this to exchange committed learning state between devices.

Required sequence:

1. Identify the active branch and reject detached HEAD.
2. Fetch `origin` when it exists.
3. Rebase the local branch onto the matching remote branch when present.
4. Validate all repository content.
5. Commit local changes only when changes exist.
6. Push the current branch without force.
7. Set upstream when the branch is new.

Rules:

- GitHub is the source of truth.
- Do not rebuild the repository from external directories.
- Do not delete untracked files to make synchronization easier.
- Do not use force-push, destructive reset, or broad checkout operations.
- Stop on a rebase conflict and report the affected files.
- Preserve unrelated local changes.
- A no-change run must succeed without creating an empty commit.

The current command is:

```bash
scripts/learn sync
```

### `study-issue`

Use this only when the agent cannot write through a local clone.

Inputs:

- Required title.
- Optional body.

Outputs:

- A public Issue in `alsrl8/mingi-miles-study` with the `inbox` label.

Rules:

- Apply the same public-content boundary used for repository files.
- Do not treat an Issue as distilled knowledge.
- Later triage the Issue into an inbox or topic note and preserve its public
  URL as provenance.

The current command is:

```bash
scripts/learn issue "Title" "Public observation"
```

### `study-distill`

Use this when a committed inbox note contains a reusable principle.

Inputs:

- Repository-relative path to a committed note below `inbox/`.
- Topic title.

Outputs:

- A new `study/<topic>-<timestamp>` branch.
- A new `topics/<topic>.md` document linked to the source note.

Rules:

- Require a clean working tree before branching.
- Reject sources outside `inbox/`.
- Never overwrite an existing topic.
- Keep the inbox note as historical evidence.
- Validate the generated topic.
- Refine substantial topic changes through a pull request before merging.

The current command is:

```bash
scripts/learn distill inbox/2026/07/example.md "Reusable topic"
```

### `study-validate`

Use this before every commit that changes content or repository behavior.

The validator must check:

- Required frontmatter in content notes.
- Valid ISO dates.
- Unique note IDs.
- `visibility: public`.
- Relative Markdown link targets.
- Common credential and private-key patterns.

The current command is:

```bash
python3 scripts/validate.py
```

Validation is a guard, not proof that a note is safe to publish. The agent still
owns the publication judgment.

### `study-review`

This capability is intentionally convention-based rather than implemented as a
single command. Agents may implement it in their own skill system.

A useful implementation should:

1. Read recent inbox notes and changed topics.
2. Identify what Miles can now explain or apply.
3. Create questions that require recall or transfer, not recognition alone.
4. Store each answer with links to the relevant topics.
5. Write a weekly review that records changed assumptions and unresolved
   questions.
6. Update a map only when a new relationship improves navigation.

Do not generate review volume for its own sake. Prefer a few questions that
reveal understanding.

## Public-content boundary

Every skill must reject or stop for material containing:

- Credentials, tokens, keys, or authentication configuration.
- Customer source documents or non-public deliverables.
- Private messages or meeting transcripts.
- Internal network locations or account details.
- Attachments that Miles does not have the right to publish.

Convert concrete work experience into a general lesson before capture. Preserve
public source attribution. When publication safety is ambiguous, do not write or
push the material; ask Miles.

## How to implement this skillset elsewhere

An agent creating equivalent local skills should follow this order:

1. Implement `study-status` and prove that it is read-only.
2. Implement `study-validate` so every later write has a shared guard.
3. Implement `study-orient` to reconstruct a study session from repository
   evidence.
4. Implement `study-capture` with unique paths and complete frontmatter.
5. Implement `study-progress` with an exact stopping point and next action.
6. Implement `study-sync` using fetch, rebase, validation, normal commit, and
   non-force push.
7. Implement `study-distill` with clean-tree and source-path guards.
8. Implement `study-issue` only when GitHub authentication is available.
9. Add `study-review` after enough real notes exist to make review useful.

The implementation may be a Codex skill, Claude skill, shell script, Python
command, MCP tool, or native application. Do not copy shell-specific details
when the target runtime offers safer primitives. Preserve the inputs, outputs,
safety rules, and observable behavior.

## Minimum verification

Before claiming an equivalent skillset is ready, demonstrate:

1. Status inspection leaves the repository unchanged.
2. Two captures made at the same time cannot overwrite each other.
3. Invalid or duplicate metadata fails validation.
4. A credential-shaped fixture is rejected without storing a real credential.
5. Sync sends a commit to a temporary remote and the remote SHA matches.
6. A no-change sync creates no commit.
7. Distillation rejects a dirty tree and sources outside `inbox/`.
8. Distillation creates a topic on a new branch and preserves the source note.
9. A progress checkpoint lets a fresh agent identify the subject, stopping
   point, unresolved questions, and next action without chat history.
10. A fresh clone passes the validator and the implementation's tests.

For this repository, run:

```bash
python3 scripts/validate.py
bash tests/test_learn.sh
git diff --check
```

An agent may claim completion only after these checks pass and the GitHub remote
contains the verified commit.
