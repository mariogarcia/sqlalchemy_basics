from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from sqlalchemy_basics import Base
from sqlalchemy_basics.utils import generate_id


class SortingBase(Base):
    # fields
    id = Column(UUID(as_uuid=True), primary_key=True)

    # meta
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        self.id = generate_id()
        super().__init__(*args, **kwargs)


class JobType(SortingBase):
    # fields
    name = Column(String(100), unique=True)

    # meta
    __tablename__ = 'jobtype'


class Country(SortingBase):
    # fields
    name = Column(String(100), unique=True)

    # meta
    __tablename__ = 'country'


class Person(SortingBase):
    # fields
    name = Column(String(100), unique=True)

    # relationships
    country_id = Column(UUID(as_uuid=True), ForeignKey("country.id"))
    country = relationship(Country, lazy='selectin')

    jobtype_id = Column(UUID(as_uuid=True), ForeignKey("jobtype.id"))
    jobtype = relationship(JobType, lazy='selectin')

    # meta
    __tablename__ = 'people'
