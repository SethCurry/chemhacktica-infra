import { useEffect, useState } from "react";
import BaseLayout from "../layouts/BaseLayout";
import { Container, listContainers } from "../api";
import { Link } from "react-router";

export default function Home() {
  const [containers, setContainers] = useState<Container[]>([]);

  useEffect(() => {
    listContainers().then((containers) => {
      setContainers(containers);
    });
  }, []);

  return (
    <BaseLayout>
      <h1>Home</h1>
      <ul>
        {containers.map((container) => (
          <li key={container.id}>
            <Link to={`/containers/${container.id}`}>
              {container.display_name}
            </Link>
          </li>
        ))}
      </ul>
    </BaseLayout>
  );
}
