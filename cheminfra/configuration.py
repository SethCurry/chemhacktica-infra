from typing import TextIO
from pydantic import BaseModel, Field


class DeploymentConfiguration(BaseModel):
    core_dir: str


class DatabaseConfiguration(BaseModel):
    url: str
    echo: bool = Field(default=False)


class DiscordConfiguration(BaseModel):
    token: str


class Configuration(BaseModel):
    deployment: DeploymentConfiguration
    database: DatabaseConfiguration
    discord: DiscordConfiguration


def load_configuration(fd: TextIO) -> Configuration:
    return Configuration.model_validate_json(fd.read())


def load_configuration_from_file(path: str) -> Configuration:
    with open(path, "r") as f:
        return load_configuration(f)


def load_default_configuration() -> Configuration:
    return load_configuration_from_file("config.json")
