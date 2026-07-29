package analyze

import (
	"testing"

	"github.com/alsrl8/mingi-miles-study/projects/agent-run-observer/llm"
	"github.com/alsrl8/mingi-miles-study/projects/agent-run-observer/utils"
)

func TestGetAiResponse(t *testing.T) {
	t.Run(
		"repository-refactor-claude",
		func(t *testing.T) {
			path := "../fixtures/synthetic/repository-refactor-claude.json"
			req, err := utils.ReadJsonFile[llm.Run](path)
			if err != nil {
				t.Errorf("failed to parse json: %+v", err)
				return
			}

			_, err = GetAiResponse(llm.Claude, *req)
			if err != nil {
				t.Errorf("failed to parse: %+v", err)
				return
			}
		})

	t.Run(
		"repository-refactor-codex",
		func(t *testing.T) {
			path := "../fixtures/synthetic/repository-refactor-codex.json"
			req, err := utils.ReadJsonFile[llm.Run](path)
			if err != nil {
				t.Errorf("failed to parse json: %+v", err)
				return
			}

			_, err = GetAiResponse(llm.Codex, *req)
			if err != nil {
				t.Errorf("failed to parse: %+v", err)
				return
			}
		})

}
