package llm

import "time"

// Run is the common representation of one synthetic agent execution.
// Vendor-specific logs can be normalized into this type later.
type Run struct {
	SchemaVersion string         `json:"schema_version"`
	RunID         string         `json:"run_id"`
	ScenarioID    string         `json:"scenario_id"`
	Engine        Provider       `json:"engine"`
	Model         string         `json:"model"`
	Task          Task           `json:"task"`
	Config        Config         `json:"config"`
	StartedAt     time.Time      `json:"started_at"`
	CompletedAt   time.Time      `json:"completed_at"`
	DurationMS    int64          `json:"duration_ms"`
	Status        string         `json:"status"`
	Usage         Usage          `json:"usage"`
	Events        []Event        `json:"events"`
	Outcome       map[string]any `json:"outcome"`
	Signals       Signals        `json:"signals"`
}

// Task describes the goal shared by runs that belong to one scenario.
type Task struct {
	Title           string   `json:"title"`
	InputKind       string   `json:"input_kind"`
	SuccessCriteria []string `json:"success_criteria"`
}

// Config contains the execution settings used by the synthetic fixtures.
// ApprovalMode and SourcePolicy are optional because they apply to different
// scenario types.
type Config struct {
	ReasoningEffort string `json:"reasoning_effort"`
	MaxToolCalls    int    `json:"max_tool_calls"`
	Parallelism     int    `json:"parallelism"`
	ApprovalMode    string `json:"approval_mode,omitempty"`
	SourcePolicy    string `json:"source_policy,omitempty"`
}

// Usage records aggregate synthetic token counts for one run.
type Usage struct {
	InputTokens       int64 `json:"input_tokens"`
	OutputTokens      int64 `json:"output_tokens"`
	CachedInputTokens int64 `json:"cached_input_tokens"`
}

// Event is one ordered action or observation within a run.
type Event struct {
	EventID         string         `json:"event_id"`
	ParentEventID   string         `json:"parent_event_id,omitempty"`
	Sequence        int            `json:"sequence"`
	Kind            string         `json:"kind"`
	Name            string         `json:"name"`
	ParallelGroup   string         `json:"parallel_group,omitempty"`
	StartedOffsetMS int64          `json:"started_offset_ms"`
	DurationMS      int64          `json:"duration_ms"`
	Status          string         `json:"status"`
	Summary         string         `json:"summary,omitempty"`
	Arguments       map[string]any `json:"arguments,omitempty"`
	Error           *EventError    `json:"error,omitempty"`
}

// EventError describes a failed or partial event.
type EventError struct {
	Category  string `json:"category"`
	Message   string `json:"message"`
	Retryable bool   `json:"retryable"`
}

// Signals stores derived counters supplied by the synthetic fixtures.
// Some counters are absent from scenarios where they are not meaningful.
type Signals struct {
	ToolCalls          int `json:"tool_calls"`
	FailedToolCalls    int `json:"failed_tool_calls"`
	RepeatedToolCalls  int `json:"repeated_tool_calls"`
	RollbackCount      int `json:"rollback_count,omitempty"`
	HumanInterventions int `json:"human_interventions,omitempty"`
	ParallelGroups     int `json:"parallel_groups,omitempty"`
	FallbackCount      int `json:"fallback_count,omitempty"`
}
