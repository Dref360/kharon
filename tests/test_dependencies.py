import pytest
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from kharon.dependencies import get_cluster
from kharon.models import User, Cluster
from kharon.models.clusters import ClusterStatus


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_has_read_access(session):
    one_user = User(email="abc@yahoo.ca")
    second_user = User(email="potato@gmail.com")
    session.add(one_user)
    session.add(second_user)
    session.commit()

    one_cluster = Cluster(creator=one_user.id, name="App Cluster", host='0.0.0.0', user_read_allow=one_user.email,
                          status=ClusterStatus.healthy)
    session.add(one_cluster)
    session.commit()
    session.refresh(one_cluster)

    assert get_cluster(cluster_name="App Cluster", user=one_user, session=session) == one_cluster
    with pytest.raises(HTTPException, match="Not Found"):
        get_cluster(cluster_name="Not there", user=one_user, session=session)

    with pytest.raises(HTTPException, match="Forbidden"):
        get_cluster(cluster_name="App Cluster", user=second_user, session=session)
