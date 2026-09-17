import pytest
from uuid import uuid4

from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from models.blogger import Blogger

from repositories.blogger_repository import BloggerRepository

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)


def test_save_blogger(session):
    repository = BloggerRepository(session)

    blogger = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    saved_blogger = repository.save_blogger(blogger)

    assert saved_blogger.id is not None
    assert saved_blogger.username == "john"
    assert saved_blogger.email == "john@gmail.com"


def test_find_blogger_by_id(session):
    repository = BloggerRepository(session)

    blogger = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    saved_blogger = repository.save_blogger(blogger)

    found_blogger = repository.find_by_id(saved_blogger.id)

    assert found_blogger is not None
    assert found_blogger.id == saved_blogger.id
    assert found_blogger.username == "john"


def test_find_blogger_by_username(session):
    repository = BloggerRepository(session)

    blogger = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    repository.save_blogger(blogger)

    found_blogger = repository.find_by_username("john")

    assert found_blogger is not None
    assert found_blogger.username == "john"


def test_find_blogger_by_email(session):
    repository = BloggerRepository(session)

    blogger = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    repository.save_blogger(blogger)

    found_blogger = repository.find_by_email("john@gmail.com")

    assert found_blogger is not None
    assert found_blogger.email == "john@gmail.com"


def test_find_blogger_by_id_returns_none_when_not_found(session):
    repository = BloggerRepository(session)

    found_blogger = repository.find_by_id(uuid4())

    assert found_blogger is None


def test_find_blogger_by_username_returns_none_when_not_found(session):
    repository = BloggerRepository(session)

    found_blogger = repository.find_by_username("does_not_exist")

    assert found_blogger is None


def test_find_blogger_by_email_returns_none_when_not_found(session):
    repository = BloggerRepository(session)

    found_blogger = repository.find_by_email("doesnotexist@gmail.com")

    assert found_blogger is None


def test_find_all_blogger(session):
    repository = BloggerRepository(session)

    blogger1 = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    blogger2 = Blogger(
        username="jane",
        email="jane@gmail.com",
        password="password456",
    )

    repository.save_blogger(blogger1)
    repository.save_blogger(blogger2)

    bloggers = repository.find_all()

    assert len(bloggers) == 2
    assert bloggers[0].username == "john"
    assert bloggers[1].username == "jane"


def test_find_all_blogger_returns_empty_list(session):
    repository = BloggerRepository(session)

    bloggers = repository.find_all()

    assert bloggers == []


def test_update_blogger(session):
    repository = BloggerRepository(session)

    blogger = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    saved_blogger = repository.save_blogger(blogger)

    saved_blogger.username = "john_updated"
    saved_blogger.email = "john_updated@gmail.com"

    updated_blogger = repository.update_blogger(saved_blogger)

    assert updated_blogger.username == "john_updated"
    assert updated_blogger.email == "john_updated@gmail.com"


def test_delete_blogger(session):
    repository = BloggerRepository(session)

    blogger = Blogger(
        username="john",
        email="john@gmail.com",
        password="password123",
    )

    saved_blogger = repository.save_blogger(blogger)

    repository.delete_blogger(saved_blogger)

    found_blogger = repository.find_by_id(saved_blogger.id)

    assert found_blogger is None