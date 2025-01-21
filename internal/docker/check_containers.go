package docker

import (
	"context"
	"fmt"
	"io"
	"slices"

	"github.com/SethCurry/chemhacktica-infra/internal/health"
	"github.com/docker/docker/api/types"
	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
)

func CheckContainers(apiClient *client.Client) ([]health.CheckResult, error) {
	containerList, err := apiClient.ContainerList(context.Background(), container.ListOptions{})
	if err != nil {
		return nil, fmt.Errorf("error listing containers: %w", err)
	}

	return checkIfContainersPresent(containerList)
}

// logChecker is a function expected to read the provided logs,
// parse them, and return a list of health check results.
type logChecker func(logs io.Reader) ([]health.CheckResult, error)

// checkLogs checks the logs of a container and
// returns a list of health check results.
// The provided checker function is responsible for
// parsing the logs and returning the results.
func checkLogs(
	apiClient *client.Client,
	containerID string,
	checker logChecker,
) ([]health.CheckResult, error) {
	logs, err := apiClient.ContainerLogs(context.Background(), containerID, container.LogsOptions{
		ShowStdout: true,
		ShowStderr: true,
	})
	if err != nil {
		return nil, fmt.Errorf("error getting logs: %w", err)
	}

	defer logs.Close()

	return checker(logs)
}

func checkIfContainersPresent(containers []types.Container) ([]health.CheckResult, error) {
	var results []health.CheckResult

	containerNames := []string{}
	for _, container := range containers {
		containerNames = append(containerNames, container.Names...)
	}

	for _, expectedContainer := range health.ExpectedContainerNames() {
		if !slices.Contains(containerNames, expectedContainer) {
			results = append(results, health.CheckResult{
				Subject: fmt.Sprintf("container %s", expectedContainer),
				Success: false,
				Message: "container not found",
			})
		}
	}

	return results, nil
}
