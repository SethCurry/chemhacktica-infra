export interface Container {
  id: number;
  display_name: string;
  container_name: string;
}

export function listContainers() {
  return fetch("/api/v1/docker/containers").then(
    (res) => res.json() as Promise<Container[]>
  );
}

export interface ContainerLogs {
  logs: string;
}

export interface ContainerStatus {
  status: string;
  recorded_at: string;
}

export function getContainerStatus(containerId: number) {
  return fetch(`/api/v1/docker/containers/${containerId}/status`).then(
    (res) => res.json() as Promise<ContainerStatus[]>
  );
}

export function getContainerLogs(containerId: number) {
  return fetch(`/api/v1/docker/containers/${containerId}/logs`).then(
    (res) => res.json() as Promise<ContainerLogs>
  );
}

export function doMakeRestart() {
  return fetch(`/api/v1/rpc/restart`).then(
    (res) => res.json() as Promise<{ message: string }>
  );
}

const defaultExport = {};

export default defaultExport;
