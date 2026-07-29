# Agent Run Observer

Agent Run Observer is a local tool for comparing AI agent executions. It should
make it easier to see where two runs differ instead of relying only on their
final answers.

## Problem

AI agent quality often becomes difficult to improve after an initial working
version. A final response alone does not show where time was spent, which tools
were repeated, or where a run diverged from another run.

The project should turn execution data into a concrete, inspectable artifact:

```text
two run logs
  -> normalize into one Go model
  -> compare steps, tool calls, timing, and failures
  -> render the differences in a simple Web UI
```

## Learning purpose

The learning surface is Go:

- model execution data with explicit types;
- parse and validate JSON;
- normalize different inputs;
- compare ordered events;
- test behavior and edge cases;
- add concurrency only when a measured use case requires it.

HTML, CSS, and JavaScript are not Miles's learning requirements for this
project. An AI agent maintains the Web UI from the Go-side contract.

The project does not require unrelated infrastructure, networking, operating
system, or frontend study. A concept enters the learning path only when a
concrete project problem requires it or Miles explicitly chooses it.

## Source of truth

Go types and their serialized output are the contract. The Web UI consumes that
contract and must not invent a second interpretation of run data.

Expected domain concepts include:

- `Run`: one complete agent execution;
- `Step`: an ordered unit within a run;
- `ToolCall`: one tool invocation and its outcome;
- `Comparison`: derived differences between two runs.

These are requirements, not completed types. Their exact fields should be
chosen from the smallest synthetic fixture that supports the first milestone.

## First milestone

M1 compares two synthetic agent runs in one local screen.

Required behavior:

1. A Go command reads two JSON files.
2. It rejects malformed input with a useful error.
3. It normalizes both inputs into the same Go model.
4. It compares total duration, step order, tool calls, repeated calls, and
   reported failures.
5. It writes a stable JSON comparison result.
6. A local Web page displays the two runs and highlights their differences.

M1 explicitly excludes:

- launching real agents;
- remote services or authentication;
- production deployment;
- automatic grading of final answers;
- storing raw private prompts in Git;
- generalized tracing or observability infrastructure.

## Public and private data

Only synthetic, reviewed fixtures belong in `fixtures/synthetic/`.

Real runs belong under:

```text
.local/agent-run-observer/runs/
```

The repository already ignores `.local/`. Never commit credentials, account
information, customer content, internal messages, private prompts, or raw tool
output that may contain them. A future importer must redact or reject unsafe
fields before producing a public fixture.

## Proposed structure

```text
agent-run-observer/
├── cmd/observer/       # executable entry point
├── internal/
│   ├── runmodel/       # Go source-of-truth types
│   ├── normalize/      # input validation and normalization
│   └── compare/        # deterministic comparison logic
├── fixtures/synthetic/
├── web/                # AI-agent-maintained presentation adapter
└── tests/
```

Create directories only when the milestone needs them. Do not scaffold empty
packages.

## Current state

The module has been initialized and contains an executable Hello World program.
Three synthetic comparison pairs exist under `fixtures/synthetic/`. No M1 Go
domain model, parser, comparison behavior, test, or Web UI has been implemented.

## Commands

Run the current program:

```bash
go run .
```

Format and test Go code:

```bash
go fmt ./...
go test ./...
```

Keep module dependencies consistent:

```bash
go mod tidy
```

## Definition of done

A milestone is complete only when:

- its observable output exists;
- related Go tests pass;
- the Web UI reflects the current Go contract;
- no private run data is tracked;
- `maps/progress.md` records the verified stopping point and next action;
- no placeholder or unimplemented requirement is described as complete.
