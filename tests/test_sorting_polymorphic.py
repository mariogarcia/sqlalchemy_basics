import pytest

from sqlalchemy_utils import sort_query
from sqlalchemy_basics.sorting.models_polymorphic import (
    SourceCountry, 
    Company, 
    ConferencePerson, 
    Atendee, 
    Speaker
)


def _create_people(db_session):
    apple = Company(name="apple")
    google = Company(name="google")

    db_session.add(apple)
    db_session.add(google)
    db_session.flush()

    france = SourceCountry(name="France")
    usa = SourceCountry(name="USA")

    db_session.add(france)
    db_session.add(usa)
    db_session.flush()

    picard = Atendee(name="Picard", company=apple, source_country=france)
    smith = Speaker(name="Smith", company=google, source_country=usa)

    db_session.add(picard)
    db_session.add(smith)
    db_session.flush()


parameters = [
    ('name', 'Picard'),
    ('-name', 'Smith'),
    ('source_country-name', 'Picard'),
    ('-source_country-name', 'Smith'),
    ('company-name', 'Picard'),
    ('-company-name', 'Smith')
]


@pytest.mark.parametrize('next', parameters)
def test_sorting_by_country(db_session, next):
    _create_people(db_session)

    # when:
    query = db_session.query(ConferencePerson).join(SourceCountry).join(Company)
    result = sort_query(query, next[0]).all()

    # then:
    assert result[0].name == next[1]
