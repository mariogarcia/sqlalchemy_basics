from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_basics import Base
from sqlalchemy.dialects.postgresql import UUID


class PetType(Base):
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100), unique=True)

    __tablename__ = 'pet_type'


class Pet(Base):
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(100))
    type = relationship("PetType")
    type_id = Column(String(100), ForeignKey("pet_type.name"))

    __tablename__ = 'pet'
    __mapper_args__ = {
        'polymorphic_identity': 'pet',
        'polymorphic_on': type_id
    }
    

class Dog(Pet):
    id = Column(UUID(as_uuid=True), ForeignKey(Pet.id), primary_key=True)
    paws = Column(Integer)

    __tablename__ = 'dog'
    __mapper_args__ = {
        'polymorphic_identity': 'dog'
    }


class Bird(Pet):
    id = Column(UUID(as_uuid=True), ForeignKey(Pet.id), primary_key=True)
    color = Column(String(100))
    night = Column(Boolean)

    __tablename__ = 'bird'
    __mapper_args__ = {
        'polymorphic_identity': 'bird'
    }