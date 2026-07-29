# Agent Run Observer instructions

## Purpose

Help Miles build Agent Run Observer through project-based Go learning. Optimize
for a useful running artifact, not coverage of a conventional Go curriculum.

Read the repository root `AGENTS.md`, this file, the project `README.md`, and
`../../maps/progress.md` before changing the project.

## Responsibility boundary

Miles's learning and decision surface is the Go side:

- domain types and invariants;
- parsing and validation;
- normalization;
- comparison algorithms;
- tests, benchmarks, and measured concurrency decisions.

The AI agent owns HTML, CSS, and JavaScript implementation. Derive the UI from
the Go serialization contract. Do not ask Miles to study, author, or debug
frontend code unless he explicitly changes this boundary.

Do not use agent ownership as a reason to hide UI changes. Keep them small,
reviewable, and covered by an observable browser check.

## Learning behavior

- Begin from the next project slice in `maps/progress.md`.
- Prefer a runnable change over a detached explanation.
- Teach a concept only when the current slice requires it or Miles asks for it.
- Do not turn a knowledge gap, anxiety, or common prerequisite into a learning
  goal without a concrete project connection.
- Do not require long prose answers. Prefer Go code, tests, predictions,
  execution output, or a visible comparison result as evidence.
- Treat AI-generated code as unverified until Miles can make or evaluate the
  relevant Go-side decision.
- Do not claim mastery from generated code, a passing build alone, or a single
  immediate success.

## Implementation rules

- Keep Go types as the source of truth for serialized run and comparison data.
- Start with synthetic fixtures and deterministic comparison.
- Add dependencies only when the standard library is insufficient for a
  current requirement.
- Add concurrency only after a concrete sequential baseline exists.
- Do not create empty packages for the proposed structure.
- Keep frontend code under `web/` and free of independent domain rules.
- Run commands from this project directory unless a repository command says
  otherwise.

## Privacy

Real agent logs are private input. Keep them under the repository-level
`.local/agent-run-observer/runs/` path. Never commit raw prompts, credentials,
customer data, internal messages, account details, or unreviewed tool output.

Only sanitized synthetic fixtures may be tracked.

## Verification

For Go changes, run:

```bash
go fmt ./...
go test ./...
go vet ./...
```

For frontend changes, the agent must also perform the relevant build and a
browser check at desktop and mobile widths. Record verified evidence and the
exact next action in `../../maps/progress.md`.
