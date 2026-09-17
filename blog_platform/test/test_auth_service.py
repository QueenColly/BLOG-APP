import pytest
from sqlmodel import SQLModel, Session, create_engine
from dtos.requests import RegisterRequest, LoginRequest
from models.user_role import Role
from repositories.admin_repository import AdminRepository
from repositories.guest_repository import GuestRepository
from repositories.blogger_repository import BloggerRepository
from services.auth_services import AuthService



engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
)


class TestAuthService:

    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            yield session

        SQLModel.metadata.drop_all(engine)

    @pytest.fixture
    def service(self, session):
        admin_repository = AdminRepository(session)
        guest_repository = GuestRepository(session)
        blogger_repository = BloggerRepository(session)

        return AuthService(
            admin_repository,
            guest_repository,
            blogger_repository,
        )
    def test_register_guest(self, service):

        data = RegisterRequest(
            username="guestone",
            email="guestone@gmail.com",
            password="password123",
            role=Role.GUEST,
        )

        guest = service.register(data)

        assert guest.id is not None
        assert guest.username == "guestone"
        assert guest.email == "guestone@gmail.com"
        assert guest.role == Role.GUEST


    def test_register_blogger(self, service):

        data = RegisterRequest(
            username="bloggerone",
            email="bloggerone@gmail.com",
            password="password123",
            role=Role.BLOGGER,
        )
        blogger = service.register(data)

        assert blogger.id is not None
        assert blogger.username == "bloggerone"
        assert blogger.email == "bloggerone@gmail.com"
        assert blogger.role == Role.BLOGGER


    def test_admin_cannot_register(self, service):

        with pytest.raises(
            PermissionError,
            match="Admin registration is not allowed",
        ):
            data = RegisterRequest(
                username="adminone",
                email="adminone@gmail.com",
                password="password123",
                role=Role.ADMIN,
            )
            service.register(data)



    def test_register_duplicate_username(self, service):

        data = RegisterRequest(
            username="john",
            email="john@gmail.com",
            password="password123",
            role=Role.GUEST,
        )
        service.register(data)

        with pytest.raises(
            ValueError,
            match="Username already exists",
        ):
            new_data = RegisterRequest(
                username="john",
                email="different@gmail.com",
                password="password456",
                role=Role.GUEST,
            )
            service.register(new_data)

    def test_register_duplicate_email(self, service):

        data = RegisterRequest(
            username="john",
            email="john@gmail.com",
            password="password123",
            role=Role.GUEST,
        )
        service.register(data)

        with pytest.raises(
            ValueError,
            match="Email already exists",
        ):
            new_data = RegisterRequest(
                username="different",
                email="john@gmail.com",
                password="password456",
                role=Role.GUEST,
            )
            service.register(new_data)

    def test_login_guest(self, service):
        register_data = RegisterRequest(
            username="guestone",
            email="guestone@gmail.com",
            password="password123",
            role=Role.GUEST,
        )

        service.register(register_data)

        login_data = LoginRequest(
            username="guestone",
            password="password123",
            role=Role.GUEST,
        )

        result = service.login(login_data)

        assert result.id is not None
        assert result.username == "guestone"
        assert result.role == Role.GUEST