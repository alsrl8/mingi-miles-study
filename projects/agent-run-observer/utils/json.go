package utils

import (
	"encoding/json"
	"fmt"
	"os"
)

func ReadJsonFile[T any](path string) (*T, error) {
	var result T

	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	err = json.NewDecoder(file).Decode(&result)
	if err != nil {
		return nil, fmt.Errorf("failed to decode json: %+v", err)
	}
	return &result, nil
}
