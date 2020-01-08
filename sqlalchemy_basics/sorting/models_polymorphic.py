from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from sqlalchemy_basics import Base
from sqlalchemy_basics.utils import generate_id


class IDBase(Base):
    # fields
    id = Column(UUID(as_uuid=True), primary_key=True)

    # meta
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        self.id = generate_id()
        super().__init__(*args, **kwargs)


class Company(IDBase):
    # fields
    name = Column(String(100), unique=True)

    # meta
    __tablename__ = 'company'


class SourceCountry(IDBase):
    # fields
    name = Column(String(100), unique=True)

    # meta
    __tablename__ = 'source_country'


class ConferencePerson(IDBase):
    # fields
    name = Column(String(100), unique=True)
    type = Column(String(100), unique=True)

    # relationships
    source_country_id = Column(UUID(as_uuid=True), ForeignKey("source_country.id"))
    source_country = relationship(SourceCountry, lazy='selectin')

    company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"))
    company = relationship(Company, lazy='selectin')

    # meta
    __tablename__ = 'conference_people'
    __mapper_args__ = {
        'polymorphic_identity': 'conference_people',
        'polymorphic_on': type
    }    


class Atendee(ConferencePerson):
    __mapper_args__ = {
        'polymorphic_identity': 'atendee'
    }    

class Speaker(ConferencePerson):
    __mapper_args__ = {
        'polymorphic_identity': 'speaker'
    }