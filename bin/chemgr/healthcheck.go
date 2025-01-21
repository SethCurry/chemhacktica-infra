package main

import (
	"github.com/SethCurry/chemhacktica-infra/internal/docker"
	"github.com/docker/docker/client"
	"go.uber.org/zap"
)

type HealthCheckCLI struct{}

// Run is the entrypoint for the HealthCheckCLI command.
// It is called as health-check on the CLI.
func (h *HealthCheckCLI) Run(bound *Bound) error {
	logger := bound.Logger
	logger.Debug("executing HealthCheckCLI")

	apiClient, err := client.NewClientWithOpts(client.FromEnv)
	if err != nil {
		return err
	}
	defer apiClient.Close()

	results, err := docker.CheckContainers(apiClient)
	if err != nil {
		return err
	}

	for _, result := range results {
		if !result.Success {
			logger.Info(result.Message, zap.String("subject", result.Subject))
		}
	}

	return nil
}
