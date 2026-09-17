from dtos.requests import RegisterRequest, LoginRequest
from dtos.responses import RegisterResponse, LoginResponse
from models.guest import Guest
from models.blogger import Blogger
from models.user_role import Role
from utils.password import hash_password, verify_password
from repositories.admin_repository import AdminRepository
from repositories.guest_repository import GuestRepository
from repositories.blogger_repository import BloggerRepository


class AuthService:

    def __init__(
        self,
        admin_repository: AdminRepository,
        guest_repository: GuestRepository,
        blogger_repository: BloggerRepository,
    ):
        self.admin_repository = admin_repository
        self.guest_repository = guest_repository
        self.blogger_repository = blogger_repository

    def register(self, data: RegisterRequest):

        if data.role == Role.ADMIN:
            raise PermissionError(
                "Admin registration is not allowed"
            )

        if data.role == Role.GUEST:

            if self.guest_repository.find_by_username(data.username):
                raise ValueError("Username already exists")

            if self.guest_repository.find_by_email(data.email):
                raise ValueError("Email already exists")

            guest = Guest(
                username=data.username,
                email=data.email,
                password=hash_password(data.password),
            )

            self.guest_repository.save_guest(guest)
            return RegisterResponse(
                id = guest.id,
                email=guest.email,
                username = guest.username,
                role = guest.role,
            )

        if data.role == Role.BLOGGER:

            if self.blogger_repository.find_by_username(data.username):
                raise ValueError("Username already exists")

            if self.blogger_repository.find_by_email(data.email):
                raise ValueError("Email already exists")

            blogger = Blogger(
                username=data.username,
                email=data.email,
                password=hash_password(data.password),
            )

            self.blogger_repository.save_blogger(blogger)
            return RegisterResponse(
                id = blogger.id,
                email=blogger.email,
                username=blogger.username,
                role=blogger.role,
            )

        raise ValueError("Invalid role")

    def login(self, data: LoginRequest) -> LoginResponse:

        if data.role == Role.ADMIN:
            user = self.admin_repository.find_by_username(data.username)

        elif data.role == Role.GUEST:
            user = self.guest_repository.find_by_username(data.username)

        elif data.role == Role.BLOGGER:
            user = self.blogger_repository.find_by_username(data.username)

        else:
            raise ValueError("Invalid role")

        if user is None:
            raise ValueError("Invalid username or password")

        if not verify_password(data.password, user.password):
            raise ValueError("Invalid username or password")

        return LoginResponse(
            id=user.id,
            username=user.username,
            role=user.role,
        )

    