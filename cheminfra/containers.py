from docker import DockerClient
from dataclasses import dataclass
from datetime import datetime

all_containers = [
		"deploy-celery_workers-1",
		"deploy-app-1",
		"retro_star",
		"mcts",
		"expand_one",
		"solubility",
		"site_selectivity",
		"scscore",
		"retro_template_relevance",
		"retro_retrosim",
		"retro_graph2smiles",
		"retro_augmented_transformer",
		"reaction_class",
		"qm_descriptors",
		"pmi_calculator",
		"pathway_ranker",
		"impurity_predictor",
		"general_selectivity",
		"forward_wldn5",
		"forward_graph2smiles",
		"forward_augmented_transformer",
		"fast_filter",
		"evaluate_reactions",
		"descriptors",
		"count_analogs",
		"context_recommender",
		"cluster",
		"atom_map_wln",
		"atom_map_rxnmapper",
		"atom_map_indigo",
		"deploy-mongo-1",
		"deploy-web-1",
		"deploy-rabbitmq-1",
		"deploy-redis-1",
]

def list_containers(client: DockerClient):
  containers = client.containers.list(all=True)
  for container in containers:
    print(container.name)
  
def find_missing_containers(client: DockerClient) -> list[str]:
  missing_containers: list[str] = []
  containers = client.containers.list(all=True)
  for container in all_containers:
    if container not in [c.name for c in containers]:
      missing_containers.append(container)
  return missing_containers

def find_not_running_containers(client: DockerClient) -> list[str]:
  not_running_containers: list[str] = []
  containers = client.containers.list()
  for container in containers:
    if container.status != "running":
      not_running_containers.append(container.name)
  return not_running_containers

@dataclass
class ApacheLog:
  timestamp: datetime
  source_ip: str
  method: str
  status: int
  path: str

def parse_apache_log_line(log_line: str) -> ApacheLog | None:
  split_line = log_line.split(" ")
  
  if len(split_line) < 9:
    return None
  
  try:
    status = int(split_line[8])
  except ValueError:
    return None
	
  timestamp = datetime.strptime(split_line[3].lstrip("["), "%d/%b/%Y:%H:%M:%S")
	
  return ApacheLog(
		timestamp=timestamp,
		source_ip=split_line[0],
		method=split_line[5].lstrip("\""),
		status=status,
		path=split_line[6],
	)

def logs_to_lines(logs: str) -> list[str]:
  return logs.split("\n")