import pytest

from pyramid import testing

from puzzle_app.models.meta import Base

from factories import FACTORIES


@pytest.yield_fixture
def app_config():
    settings = {'sqlalchemy.url': 'sqlite:///:memory:'}
    config = testing.setUp(settings=settings)
    config.include('puzzle_app.models')
    yield config
    testing.tearDown()


@pytest.fixture
def db_session(app_config):
    session = app_config.registry['dbsession_factory']()
    engine = session.bind
    Base.metadata.create_all(engine)
    return session


@pytest.fixture
def dummy_request(db_session):
    return testing.DummyRequest(db_session=db_session)


@pytest.fixture(autouse=True)
def set_sqlalchemy_session_on_factories(db_session):
    for factory_cls in FACTORIES:
        factory_cls._meta.sqlalchemy_session = db_session
