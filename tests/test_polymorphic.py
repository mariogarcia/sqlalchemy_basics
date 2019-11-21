from sqlalchemy.orm import with_polymorphic
from sqlalchemy_basics.polymorphic.models import Bird, Dog, Pet, PetType
from sqlalchemy_basics.utils import generate_id


def test_insert(db_session):
    birds = PetType(id=generate_id(), name="bird")
    db_session.add(birds)
    db_session.flush()

    eagle = Bird(id=generate_id(), name="eagle", type=birds)
    db_session.add(eagle)
    db_session.flush()

    AllPets = with_polymorphic(Pet, [Bird, Dog])
    pets = db_session.query(AllPets).all()
    
    assert len(pets) == 1