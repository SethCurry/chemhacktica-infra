package docker

import (
	"context"
	"fmt"
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

func checkIfContainersPresent(containers []types.Container) ([]health.CheckResult, error) {
	expectedContainers := []string{
		"/deploy-celery_workers-1",
		"/deploy-app-1",
		"/retro_star",
		"/mcts",
		"/expand_one",
		"/solubility",
		"/site_selectivity",
		"/scscore",
		"/retro_template_relevance",
		"/retro_retrosim",
		"/retro_graph2smiles",
		"/retro_augmented_transformer",
		"/reaction_class",
		"/qm_descriptors",
		"/pmi_calculator",
		"/pathway_ranker",
		"/impurity_predictor",
		"/general_selectivity",
		"/forward_wldn5",
		"/forward_graph2smiles",
		"/forward_augmented_transformer",
		"/fast_filter",
		"/evaluate_reactions",
		"/descriptors",
		"/count_analogs",
		"/context_recommender",
		"/cluster",
		"/atom_map_wln",
		"/atom_map_rxnmapper",
		"/atom_map_indigo",
		"/deploy-mongo-1",
		"/deploy-web-1",
		"/deploy-rabbitmq-1",
		"/deploy-redis-1",
	}

	var results []health.CheckResult

	containerNames := []string{}
	for _, container := range containers {
		containerNames = append(containerNames, container.Names...)
	}

	for _, expectedContainer := range expectedContainers {
		if !slices.Contains(containerNames, expectedContainer) {
			results = append(results, health.CheckResult{
				Success: false,
				Message: fmt.Sprintf("container %s not found", expectedContainer),
			})
		}
	}

	return results, nil
}
