import fire
import logging
import structlog
import docker

from cheminfra.containers import parse_apache_log_line, find_missing_containers, find_not_running_containers

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False
)
log = structlog.get_logger()


class CLI:
    def health(self):
        client = docker.from_env()
        missing_containers = find_missing_containers(client)
        not_running_containers = find_not_running_containers(client)
        for container in missing_containers:
            log.error("container is missing", container=container)

        for container in not_running_containers:
            log.error("container is not running", container=container)

        for container in client.containers.list():
            if container.name == "deploy-web-1":
                logs = str(container.logs()).split("\\n")
                for log_line in logs:
                    try:
                        parsed = parse_apache_log_line(log_line)
                        if parsed and parsed.status == 500:
                            print(parsed)
                    except Exception as e:
                        log.error("error parsing log line", log_line=log_line, error=e)
            #print(container.name, container.status)

if __name__ == "__main__":
    fire.Fire(CLI)
