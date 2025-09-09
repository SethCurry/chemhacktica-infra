import structlog
from cheminfra.ingest.scheduler import scheduler
from sqlalchemy.orm import Session
from dataclasses import dataclass
import docker

from cheminfra.db.containers import Container, ContainerStatus


@dataclass
class DefaultContainer:
    display_name: str
    container_name: str


@scheduler.add_task("register-containers")
def register_all_containers(session: Session):
    logger = structlog.get_logger(task="register-containers")
    all_containers: list[DefaultContainer] = [
        DefaultContainer("Celery Workers", "deploy-celery_workers-1"),
        DefaultContainer("App", "deploy-app-1"),
        DefaultContainer("Retro Star", "retro_star"),
        DefaultContainer("MCTS", "mcts"),
        DefaultContainer("Expand One", "expand_one"),
        DefaultContainer("Solubility", "solubility"),
        DefaultContainer("Site Selectivity", "site_selectivity"),
        DefaultContainer("SCScore", "scscore"),
        DefaultContainer("Retro Template Relevance", "retro_template_relevance"),
        DefaultContainer("Retro RetroSim", "retro_retrosim"),
        DefaultContainer("Retro Graph2SMILES", "retro_graph2smiles"),
        DefaultContainer("Retro Augmented Transformer", "retro_augmented_transformer"),
        DefaultContainer("Reaction Class", "reaction_class"),
        DefaultContainer("QM Descriptors", "qm_descriptors"),
        DefaultContainer("PMI Calculator", "pmi_calculator"),
        DefaultContainer("Pathway Ranker", "pathway_ranker"),
        DefaultContainer("Impurity Predictor", "impurity_predictor"),
        DefaultContainer("General Selectivity", "general_selectivity"),
        DefaultContainer("Forward WLDN5", "forward_wldn5"),
        DefaultContainer("Forward Graph2SMILES", "forward_graph2smiles"),
        DefaultContainer(
            "Forward Augmented Transformer", "forward_augmented_transformer"
        ),
        DefaultContainer("Fast Filter", "fast_filter"),
        DefaultContainer("Evaluate Reactions", "evaluate_reactions"),
        DefaultContainer("Descriptors", "descriptors"),
        DefaultContainer("Count Analogs", "count_analogs"),
        DefaultContainer("Context Recommender", "context_recommender"),
        DefaultContainer("Cluster", "cluster"),
        DefaultContainer("Atom Map WLN", "atom_map_wln"),
        DefaultContainer("Atom Map RxnMapper", "atom_map_rxnmapper"),
        DefaultContainer("Atom Map Indigo", "atom_map_indigo"),
        DefaultContainer("Mongo", "deploy-mongo-1"),
        DefaultContainer("Web", "deploy-web-1"),
        DefaultContainer("RabbitMQ", "deploy-rabbitmq-1"),
        DefaultContainer("Redis", "deploy-redis-1"),
    ]

    for container in all_containers:
        existing = (
            session.query(Container)
            .filter(Container.container_name == container.container_name)
            .one_or_none()
        )
        if existing:
            logger.debug("container already exists", container=container)
            existing.display_name = container.display_name
        else:
            logger.debug("container does not exist", container=container)
            session.add(
                Container(
                    display_name=container.display_name,
                    container_name=container.container_name,
                )
            )
        session.commit()


@scheduler.add_task("get-container-status")
def get_container_status(session: Session):
    logger = structlog.get_logger(task="get-container-status")
    containers = session.query(Container).all()
    for container in containers:
        logger.debug("container status", container=container)
        client = docker.from_env()
        got_container = client.containers.get(container.container_name)

        prior_status = (
            session.query(ContainerStatus)
            .filter(ContainerStatus.container_id == container.id)
            .order_by(ContainerStatus.recorded_at.desc())
            .first()
        )
        if prior_status and prior_status.status == got_container.status:
            logger.debug("status is the same", container=container)
            continue
        new_status = ContainerStatus(
            status=got_container.status, container_id=container.id
        )
        session.add(new_status)
        session.commit()
