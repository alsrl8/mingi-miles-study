package analyze

import (
	"fmt"

	"github.com/alsrl8/mingi-miles-study/projects/agent-run-observer/llm"
)

type AiResponse struct {
	MetaData struct {
		Engine string
		Model  string
		Task   struct {
			Title           string
			InputKind       string
			SuccessCriteria []string
		}
	}
	TotalDurationMs int
	TotalUsage      struct {
		InputTokens       int
		OutputTokens      int
		CachedInputTokens int
	}
	Events []Event
}

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

type EventError struct {
	Category  string `json:"category"`
	Message   string `json:"message"`
	Retryable bool   `json:"retryable"`
}

func validateProvider(p llm.Provider) error {
	switch p {
	case llm.Claude:
		fmt.Printf("claude")
		return nil
	case llm.Codex:
		fmt.Printf("codex")
		return nil
	default:
		return fmt.Errorf("unsupported provider %s", string(p))
	}
}

func GetAiResponse(p llm.Provider, r llm.Run) (*AiResponse, error) {
	if err := validateProvider(p); err != nil {
		return nil, err
	}

	var resp AiResponse

	resp.MetaData.Engine = string(p)
	resp.MetaData.Model = r.Model
	resp.MetaData.Task = struct {
		Title           string
		InputKind       string
		SuccessCriteria []string
	}{
		Title:           r.Task.Title,
		InputKind:       r.Task.InputKind,
		SuccessCriteria: r.Task.SuccessCriteria,
	}

	resp.TotalDurationMs = int(r.DurationMS)
	resp.TotalUsage = struct {
		InputTokens       int
		OutputTokens      int
		CachedInputTokens int
	}{
		InputTokens:       int(r.Usage.InputTokens),
		OutputTokens:      int(r.Usage.OutputTokens),
		CachedInputTokens: int(r.Usage.CachedInputTokens),
	}

	return &resp, nil
}
