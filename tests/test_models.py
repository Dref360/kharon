import pytest
from fastapi import HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from kharon.auth import create_api_key, disable_api_key
from kharon.dependencies import get_current_user
from kharon.models import User, Cluster, Job, APIKey
from kharon.models.clusters import ClusterStatus
from kharon.models.jobs import JobDescription


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

    one_cluster = Cluster(creator=one_user.id, name="App Cluster", host='0.0.0.0', user_read_allow=one_user.email,
                          status=ClusterStatus.healthy)
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


def test_api_token(session):
    one_user = User(email="abc.yahoo.ca")
    session.add(one_user)
    session.commit()

    api_key = create_api_key(one_user.id, key_name='key1', session=session)
    assert api_key.startswith('ss-')
    keys = session.exec(select(APIKey).where(APIKey.user_id == one_user.id)).all()
    assert len(keys) == 1
    # Assert that we don't store keys in plain text
    assert keys[0].user_id == one_user.id and keys[0].hashed_key != api_key and keys[0].is_active

    assert get_current_user(token=api_key, session=session) == one_user
    with pytest.raises(HTTPException, match='404'):
        get_current_user(token='ss-potato', session=session)

    disable_api_key(one_user.id, key_name='key1', session=session)
    updated_key = session.exec(select(APIKey).where(APIKey.user_id == one_user.id)).first()
    assert updated_key is not None
    assert not updated_key.is_active

    with pytest.raises(HTTPException, match='404'):
        # Disabled so can't find it.
        get_current_user(token=api_key, session=session)
