import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from shared_science.models import User, Cluster, Job
from shared_science.models.jobs import JobDescription


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_jobs(session: Session):

    one_user = User(email="abc.yahoo.ca")
    session.add(one_user)
    session.commit()

    one_cluster = Cluster(creator=one_user.id, name="App Cluster")
    session.add(one_cluster)
    session.commit()

    job = Job(creator=one_user.id, cluster=one_cluster.id, name="Super App",
              job_description=JobDescription(image="nginx"))
    session.add(job)
    session.commit()

    jobs = session.exec(select(Job).where(Job.creator == 'not_real_id')).all()
    assert len(jobs) == 0

    jobs = session.exec(select(Job).where(Job.creator == one_user.id)).all()
    assert len(jobs) == 1 and jobs[0].name == "Super App"
