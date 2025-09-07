import subprocess
from fastapi import FastAPI, Depends

from cheminfra.configuration import load_default_configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, joinedload
from contextlib import asynccontextmanager
from typing import Annotated

from cheminfra.db.containers import Container, ContainerStatus

config = load_default_configuration()

engine = create_engine(config.database.url, echo=config.database.echo)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)


async def get_session():
    session = Session(engine)
    yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/api/v1/docker/containers")
def get_containers(session: SessionDep):
    containers = session.query(Container).all()
    return containers


@app.get("/api/v1/docker/containers/{container_id}/status")
def get_container_status(container_id: int, session: SessionDep):
    statuses = (
        session.query(ContainerStatus)
        .filter(ContainerStatus.container_id == container_id)
        .order_by(ContainerStatus.recorded_at.desc())
        .limit(100)
        .all()
    )
    return statuses


@app.get("/api/v1/docker/containers/{container_id}")
def get_container(container_id: int, session: SessionDep):
    container = (
        session.query(Container)
        .filter(Container.id == container_id)
        .join(ContainerStatus)
        .options(joinedload(Container.statuses))
        .one_or_none()
    )
    return container


@app.get("/api/healthcheck")
def healthcheck():
    return {"message": "OK"}


@app.get("/api/v1/rpc/restart")
def make_restart():
    try:
        subprocess.run(["make", "restart"], cwd=config.deployment.core_dir, check=True)
        return {"message": "Restarted successfully"}
    except subprocess.CalledProcessError as e:
        return {"message": "Failed to restart", "error": str(e)}
