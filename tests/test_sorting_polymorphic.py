import pytest

from sqlalchemy.orm import aliased
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
    misft = Company(name="microsoft")
    kaleidos = Company(name="Kaleidos")

    db_session.add_all([apple, google, misft])
    db_session.flush()

    france = SourceCountry(name="France")
    spain = SourceCountry(name="Spain")
    usa = SourceCountry(name="USA")
    uk = SourceCountry(name="UK")
    canada = SourceCountry(name="Canada")

    db_session.add_all([france, usa, spain, uk, canada])
    db_session.flush()

    picard = Atendee(name="Picard", company=apple, source_country=france)
    smith = Speaker(name="Smith", company=google, source_country=uk)
    john = Speaker(name="John", company=google, source_country=usa)
    peter = Atendee(name="Peter", company=google, source_country=canada)
    mario = Atendee(name="Mario", company=kaleidos, source_country=spain)

    db_session.add_all([picard, smith, john, peter, mario])
    db_session.flush()


parameters = [
    ('name', 'John'),
    ('-name', 'Smith'),
    ('source_country-name', 'Peter'),
    ('-source_country-name', 'John'),
    ('company-name', 'Picard'),
    ('-company-name', 'Mario')
]


@pytest.mark.parametrize('next', parameters)
def test_sorting_by_country(db_session, next):
    # given: a bunch of people
    _create_people(db_session)

    # the name of the property we want to sort by must
    # match the name of the name of the joined table
    # here we've created an alias because the table is
    # named 'companies' and the sort_by property is `company`
    joined_company = aliased(Company, name='company')

    query = db_session.\
        query(ConferencePerson).\
        join(SourceCountry).\
        join(joined_company)

    # when: sorting by the current criteria
    result = sort_query(query, next[0]).all()

    # then: we should get the expected result
    assert result[0].name == next[1]


def test_filtering_by_company_and_sorting_by_country(db_session):
    # given: a bunch of people
    _create_people(db_session)

    # because we're not sorting by company there's no
    # need to create an alias, but it would be
    # advisable to do so just in case
    query = db_session.\
        query(ConferencePerson).\
        join(SourceCountry).\
        join(Company).\
        filter(Company.name == 'google')

    # when: sorting the query by country's name
    result = sort_query(query, 'source_country-name').all()

    # then: we should get the expected person
    assert result[0].name == 'Peter'
