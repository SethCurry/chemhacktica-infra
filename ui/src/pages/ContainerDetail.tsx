import { useParams } from "react-router";
import { ContainerStatus, getContainerLogs, getContainerStatus } from "../api";
import { useEffect, useState } from "react";
import BaseLayout from "../layouts/BaseLayout";

export default function ContainerDetail() {
  const { containerId } = useParams();
  const [logs, setLogs] = useState<string>("");
  const [statuses, setStatuses] = useState<ContainerStatus[]>([]);

  useEffect(() => {
    const parsedContainerId = parseInt(containerId ?? "0");
    getContainerLogs(parsedContainerId).then((gotLogs) => {
      setLogs(gotLogs.logs);
    });
    getContainerStatus(parsedContainerId).then((gotStatuses) => {
      setStatuses(gotStatuses);
    });
  }, [containerId]);
  return (
    <BaseLayout>
      <h2>Statuses</h2>
      <table style={{ borderCollapse: "collapse", textAlign: "center" }}>
        <thead>
          <tr>
            <th>Status</th>
            <th>Since</th>
          </tr>
        </thead>
        <tbody>
          {statuses.map((status) => (
            <tr key={status.recorded_at}>
              <td style={{ border: "1px solid black" }}>{status.status}</td>
              <td style={{ border: "1px solid black" }}>
                {status.recorded_at}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Logs</h2>
      <pre style={{ whiteSpace: "pre-wrap" }}>{logs}</pre>
    </BaseLayout>
  );
}
