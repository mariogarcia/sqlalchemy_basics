import pytest

from sqlalchemy import create_engine, Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import scoped_session, sessionmaker
from testcontainers.postgres import PostgresContainer

from sqlalchemy_basics import Base

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