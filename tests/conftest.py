import pytest

from logging.config import dictConfig
from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from testcontainers.postgres import PostgresContainer
from yaml import Loader, YAMLError, add_constructor, load

from sqlalchemy_basics import Base


@pytest.fixture(scope="session", autouse=True)
def config_logging():
    try:
        with open('tests/logging.yaml', 'r') as ymlfile:
            yaml = load(ymlfile, Loader=Loader)
            dictConfig(yaml)
    except YAMLError:
        log.error("error while parsing yaml")
        raise
    except FileNotFoundError:
        log.error("config file not found")
        raise    


@pytest.fixture(scope="session")
def db_session(request):
    postgres = PostgresContainer()
    postgres.start()

    db_url = postgres.get_connection_url()
    engine = create_engine(db_url)

    session = scoped_session(
        sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine))

    Base.query = session.query_property()
    Base.metadata.create_all(engine)

    def stop_db():
        postgres.stop()

    request.addfinalizer(stop_db)

    return session


@pytest.fixture(scope="function", autouse=True)
def cleanup(request, db_session):
    """
    Trunc all tables at the end of each test
    """
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())

    def function_ends():
        db_session.commit()
        db_session.close()

    request.addfinalizer(function_ends)