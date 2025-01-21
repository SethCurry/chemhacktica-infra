package main

import (
	"github.com/alecthomas/kong"
	"go.uber.org/zap"
)

type (
	CLI struct {
		HealthCheck HealthCheckCLI `cmd:"healthcheck" help:"Check the health of the ChemHacktica services"`
	}

	Bound struct {
		Logger *zap.Logger
	}
)

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
