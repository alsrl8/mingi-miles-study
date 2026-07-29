# Synthetic run fixtures

These files are invented inputs for Agent Run Observer. They do not reproduce a
current Codex, Claude, or other vendor log format. Names such as `codex` and
`claude` are scenario labels that make each pair easy to discuss.

The fixtures are intentionally richer than the first Go parser needs. Start by
reading only:

- `schema_version`;
- `run_id`;
- `scenario_id`;
- `duration_ms`;
- `status`;
- `events`.

Add fields to the Go model only when a comparison requirement needs them. The
Go model remains the eventual source of truth; this mock shape is discovery
input, not a permanent external contract.

## Comparison pairs

| Scenario | Run A | Run B | Useful differences |
| --- | --- | --- | --- |
| Test failure diagnosis | `test-failure-codex.json` | `test-failure-claude.json` | focused search versus repeated broad search and retry |
| Repository refactor | `repository-refactor-codex.json` | `repository-refactor-claude.json` | parallel exploration versus sequential work and rollback |
| Technical research | `technical-research-codex.json` | `technical-research-claude.json` | primary-source path versus fallback and duplicate collection |

## Shape

Each file contains:

- run identity and scenario identity;
- mock engine and model labels;
- configuration that may explain execution differences;
- aggregate timing and token usage;
- an ordered `events` list;
- a final outcome and quality signals.

Events use these kinds:

- `assistant`: a visible or internal agent action summary;
- `decision`: a branch in the execution strategy;
- `tool_call`: a requested tool invocation;
- `tool_result`: its result;
- `checkpoint`: an intermediate state or verification point.

`parent_event_id` connects a tool result to its call. `parallel_group` marks
events that were allowed to overlap. Durations and token counts are synthetic.

Real run logs must stay under the repository-level
`.local/agent-run-observer/runs/` directory.
