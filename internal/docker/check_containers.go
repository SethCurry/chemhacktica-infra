package docker

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"strconv"
	"strings"
	"time"

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

	results, err := checkIfContainersPresent(containerList)
	if err != nil {
		return nil, fmt.Errorf("error checking if containers are present: %w", err)
	}

	httpErrorResults, err := checkHTTPErrorCount(context.Background(), apiClient, "deploy-web-1", 5, 1*time.Hour)
	if err != nil {
		return nil, fmt.Errorf("error checking HTTP error count: %w", err)
	}

	results = append(results, httpErrorResults...)

	return results, nil
}

// logChecker is a function expected to read the provided logs,
// parse them, and return a list of health check results.
type logChecker func(logs io.Reader) ([]health.CheckResult, error)

func checkHTTPErrorCount(ctx context.Context, apiClient *client.Client, containerID string, maxErrors int, lookback time.Duration) ([]health.CheckResult, error) {
	logs, err := apiClient.ContainerLogs(ctx, containerID, container.LogsOptions{
		ShowStdout: true,
		ShowStderr: true,
		Since:      time.Now().Add(-lookback).Format(time.RFC3339),
	})
	if err != nil {
		return nil, fmt.Errorf("error getting logs: %w", err)
	}

	defer logs.Close()

	errorCount, err := getHTTPErrorCount(logs, lookback)
	if err != nil {
		return nil, fmt.Errorf("error getting HTTP error count: %w", err)
	}

	if errorCount > maxErrors {
		return []health.CheckResult{
			{
				Subject: fmt.Sprintf("container %s", containerID),
				Success: false,
				Message: fmt.Sprintf("HTTP error count exceeded: %d", errorCount),
			},
		}, nil
	}

	return nil, nil
}

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

type parsedHTTPLogLine struct {
	SourceIP  string
	Timestamp time.Time
	Method    string
	Path      string
	Status    int
}

func getHTTPErrorCount(logs io.Reader, lookback time.Duration) (int, error) {
	scanner := bufio.NewScanner(logs)

	errorCount := 0

	for scanner.Scan() {
		line := scanner.Text()
		parsed, err := parseHTTPLogLine(line)
		if err != nil {
			return 0, fmt.Errorf("error parsing log line: %w", err)
		}

		if parsed.Status >= 500 && parsed.Timestamp.After(time.Now().Add(-lookback)) {
			errorCount++
		}
	}

	return errorCount, nil
}

func parseHTTPLogLine(line string) (*parsedHTTPLogLine, error) {
	// Sample log line
	// 172.69.214.214 - - [17/Dec/2024:03:14:51 +0000] "GET /api/legacy/celery/task/c139737b-2661-4c0a-b745-11d4db84d0df/ HTTP/1.1" 200 149 "https://synth.fourthievesvinegar.org/network?tab=IPP&target=Clc1cc2c(cc1)N(C(%3DO)N2)C5CCN(CCCN4c3ccccc3NC4%3DO)CC5" "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0"
	parts := strings.Split(line, " ")

	statusInt, err := strconv.Atoi(parts[8])
	if err != nil {
		return nil, fmt.Errorf("error parsing status: %w", err)
	}

	timestamp, err := time.ParseInLocation("02/Jan/2006:15:04:05", strings.TrimLeft(parts[3], "["), time.UTC)
	if err != nil {
		return nil, fmt.Errorf("error parsing timestamp %s: %w", line, err)
	}

	resp := parsedHTTPLogLine{
		SourceIP:  parts[0],
		Method:    strings.TrimLeft(parts[5], "\""),
		Path:      parts[6],
		Status:    statusInt,
		Timestamp: timestamp,
	}

	return &resp, nil
}

func checkIfContainersPresent(containers []types.Container) ([]health.CheckResult, error) {
	var results []health.CheckResult

	containerNames := []string{}
	for _, container := range containers {
		containerNames = append(containerNames, container.Names...)
	}

	for _, expectedContainer := range health.ExpectedContainerNames() {
		found := false
		for _, cont := range containers {
			for _, name := range cont.Names {
				if name == expectedContainer {
					found = true

					if cont.State != "running" {
						results = append(results, health.CheckResult{
							Subject: fmt.Sprintf("container %s", expectedContainer),
							Success: false,
							Message: "container not running",
						})
					}
					break
				}
			}
		}

		if !found {
			results = append(results, health.CheckResult{
				Subject: fmt.Sprintf("container %s", expectedContainer),
				Success: false,
				Message: "container not found",
			})
		}
	}

	return results, nil
}
