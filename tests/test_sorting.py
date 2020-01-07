import pytest

from sqlalchemy_utils import sort_query
from sqlalchemy_basics.sorting.models import Country, JobType, Person


def _create_people(db_session):
    unknown = JobType(name="unknown")
    soldier = JobType(name="soldier")

    db_session.add(unknown)
    db_session.add(soldier)
    db_session.flush()

    france = Country(name="France")
    usa = Country(name="USA")

    db_session.add(france)
    db_session.add(usa)
    db_session.flush()

    amelie = Person(name="Amelie", jobtype=unknown, country=france)
    rambo = Person(name="Rambo", jobtype=soldier, country=usa)

    db_session.add(amelie)
    db_session.add(rambo)
    db_session.flush()


parameters = [
    ('name', 'Amelie'),
    ('-name', 'Rambo'),
    ('country-name', 'Amelie'),
    ('-country-name', 'Rambo'),
    ('jobtype-name', 'Rambo'),
    ('-jobtype-name', 'Amelie')
]


@pytest.mark.parametrize('next', parameters)
def test_sorting_by_country(db_session, next):
    _create_people(db_session)

    # when:
    query = db_session.query(Person).join(Country).join(JobType)
    result = sort_query(query, next[0]).all()

    # then:
    assert result[0].name == next[1]
