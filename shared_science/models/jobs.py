from enum import Enum
from typing import Optional, List

from sqlmodel import Field, SQLModel, Column

from shared_science.models.model_utils import pydantic_column_type  # type: ignore


# NOTE: Could reuse another library for this state management.
class JobStatus(str, Enum):
    not_started = "not_started"
    running = "running"
    done = "done"


class JobResources(SQLModel):
    cpu: int = 1
    mem: int = 1  # In GBs


class JobDescription(SQLModel):
    image: str
    command: List[str] = []
    resources: JobResources = JobResources()


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creator: Optional[int] = Field(default=None, foreign_key="user.id")
    cluster: Optional[int] = Field(default=None, foreign_key="cluster.id")
    name: str
    status: JobStatus = JobStatus.not_started
    job_description: JobDescription = Field(
        ..., sa_column=Column(pydantic_column_type(JobDescription))
    )
