from enum import Enum
from typing import Optional

from pydantic.v1 import BaseModel
from sqlmodel import Field

from kharon.models.model_utils import ResourceSQLModel


class ClusterStatus(str, Enum):
    healthy = "healthy"
    not_healthy = "not_healthy"


class ClusterType(str, Enum):
    # TODO We should be able to add to this enum for custom setup.
    docker = "docker"


class Cluster(ResourceSQLModel, table=True):  # type: ignore
    creator: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    host: str
    remote_host: str
    status: ClusterStatus
    # Unused for now
    type: ClusterType = ClusterType.docker


class HealthCheck(BaseModel):
    local_service_alive: bool
    ssh_service_alive: bool
