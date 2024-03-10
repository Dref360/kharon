from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field


class ClusterType(str, Enum):
    # TODO We should be able to add to this enum for custom setup.
    docker = "docker"


class Cluster(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator: Optional[int] = Field(default=None, foreign_key="user.id")
    name: str
    type: ClusterType = ClusterType.docker
