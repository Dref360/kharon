import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from shared_science.iam import has_access_to_resource
from shared_science.models import User, Cluster
from shared_science.models.clusters import ClusterStatus


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

    assert has_access_to_resource(one_user.email, one_cluster)
    assert not has_access_to_resource(second_user.email, one_cluster)

    one_cluster.add_user(second_user.email, session)
    assert has_access_to_resource(one_user.email, one_cluster)
    assert has_access_to_resource(second_user.email, one_cluster)
