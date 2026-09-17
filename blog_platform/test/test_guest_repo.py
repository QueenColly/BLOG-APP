import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import uuid
from sqlmodel import SQLModel, Session, create_engine
from models.guest import Guest
from repositories.guest_repository import GuestRepository

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_that_if_i_find_a_user_by_email_it_returns_the_correct_user(session: Session):
    repo = GuestRepository(session)

    guest = Guest(id=uuid.uuid4(), username="gampLite", email="gamplatitude", password="gamp@3000")
    repo.save_guest(guest)

    found_guest = repo.find_by_email("gamplatitude")

    assert found_guest is not None
    assert found_guest.username == "gampLite"

def test_that_i_save_and_find_guest_by_id(session: Session):
    repo = GuestRepository(session)

    guest_id = uuid.uuid4()
    new_guest = Guest(id=guest_id, username="chloe30", email="chloe@3000", password="Linux@3000")

    saved_guest = repo.save_guest(new_guest)
    assert saved_guest.id is not None

    found_guest = repo.find_by_id(guest_id)
    assert found_guest is not None
    assert found_guest.id == guest_id
    assert found_guest.email == "chloe@3000"

def test_that_i_save_and_find_guest_by_id_and_does_not_exist(session: Session):
    repo = GuestRepository(session)
    guest_id = uuid.uuid4()

    found_guest = repo.find_by_id(guest_id)
    assert found_guest is None

def test_that_i_save_and_find_guest_by_email_and_does_not_exist(session: Session):
    repo = GuestRepository(session)

    found_guest = repo.find_by_email("william-cockburn")
    assert found_guest is None
