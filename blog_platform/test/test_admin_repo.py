import pytest
from sqlmodel import SQLModel, Session, create_engine
from models.admin import Admin
from repositories.admin_repository import AdminRepository

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
)


class TestAdminRepository:

    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            yield session
        SQLModel.metadata.drop_all(engine)

    def test_save_admin(self, session):
        repository = AdminRepository(session)
        admin = Admin(
            username = "admin",
            email = "admin@gmail.com",
            password = "password",
        )
        saved_admin = repository.save_admin(admin)

        assert saved_admin.username == "admin"
        assert saved_admin.email == "admin@gmail.com"

    def test_find_by_id(self, session):
        repository = AdminRepository(session)
        admin = Admin(
            username="admintwo",
            email="admintwo@gmail.com",
            password="passwordtwo",
        )
        saved_admin = repository.save_admin(admin)
        found_admin = repository.find_by_id(saved_admin.id)

        assert found_admin.id == saved_admin.id


    def test_find_by_username(self, session):
        repository = AdminRepository(session)
        admin = Admin(
            username="adminthree",
            email="adminthree@gmail.com",
            password="passwordthree",
        )
        saved_admin = repository.save_admin(admin)
        found_admin = repository.find_by_username(saved_admin.username)

        assert found_admin.username == saved_admin.username


    def test_find_by_email(self, session):
        repository = AdminRepository(session)
        admin = Admin(
            username="adminfour",
            email="adminfour@gmail.com",
            password="passwordfour",
        )
        saved_admin = repository.save_admin(admin)
        found_admin = repository.find_by_email(saved_admin.email)

        assert found_admin.email == saved_admin.email

    def test_find_all(self, session):
        repository = AdminRepository(session)
        admin1 = Admin(
            username="adminfive",
            email="adminfive@gmail.com",
            password="passwordfive",
        )
        admin2 = Admin(
            username="adminsix",
            email="adminsix@gmail.com",
            password="passwordsix",
        )
        first_saved = repository.save_admin(admin1)
        second_saved = repository.save_admin(admin2)
        admins = repository.find_all()

        assert len(admins) == 2
        assert admins[0].username == first_saved.username
        assert admins[1].username == second_saved.username

    def test_update_admin(self, session):
        repository = AdminRepository(session)
        admin = Admin(
            username="old_username",
            email="old@gmail.com",
            password="passwordold",
        )
        saved_admin = repository.save_admin(admin)
        saved_admin.username = "new_username"
        saved_admin.email = "new@gmail.com"
        updated_admin = repository.update_admin(saved_admin)

        assert updated_admin.username == "new_username"
        assert updated_admin.email == "new@gmail.com"


    def test_delete_admin(self, session):
        repository = AdminRepository(session)
        admin = Admin(
            username="delete_admin",
            email="delete@gmail.com",
            password="password",
        )
        saved_admin = repository.save_admin(admin)
        repository.delete_admin(saved_admin)
        found_admin = repository.find_by_id(saved_admin.id)

        assert found_admin is None
