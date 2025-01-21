package main

import (
	"github.com/SethCurry/chemhacktica-infra/internal/docker"
	"github.com/alecthomas/kong"
	"github.com/docker/docker/client"
	"go.uber.org/zap"
)

type (
	HealthCheckCLI struct{}
	CLI            struct {
		HealthCheck HealthCheckCLI `cmd:"healthcheck" help:"Check the health of the ChemHacktica services"`
	}

	Bound struct {
		Logger *zap.Logger
	}
)

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

func main() {
	cfg := zap.NewProductionConfig()

	cfg.Level.SetLevel(zap.DebugLevel)
	cfg.Encoding = "console"
	cfg.OutputPaths = []string{"stdout"}

	logger, err := cfg.Build()
	if err != nil {
		panic(err)
	}

	var cli CLI

	parsed := kong.Parse(&cli)

	bound := Bound{
		Logger: logger,
	}

	err = parsed.Run(&bound)
	if err != nil {
		logger.Error("error running command", zap.Error(err))
	}
}
