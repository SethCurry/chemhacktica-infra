import fire
import logging
import structlog
import docker

from cheminfra.containers import parse_apache_log_line

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
        containers = client.containers.list(all=True)
        for container in containers:
            if container.status != "running":
                log.error("container is not running", container=container.name)
                continue
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
