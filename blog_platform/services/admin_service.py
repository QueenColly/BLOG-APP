from models.admin import Admin
from dtos.requests import CreateAdminRequest
from dtos.responses import CreateAdminResponse
from models.user_role import Role
from repositories.admin_repository import AdminRepository
from utils.password import hash_password, verify_password


class AdminService:

    def __init__(self, repository: AdminRepository):
        self.repository = repository

    def create_first_admin(self, data: CreateAdminRequest):
        existing_admins = self.repository.find_all()

        if existing_admins:
            raise ValueError("An admin already exists")

        admin = Admin(
            username=data.username,
            email=data.email,
            password=hash_password(data.password)
        )

        self.repository.save_admin(admin)
        return CreateAdminResponse(
            id = admin.id,
            email = admin.email,
            username = admin.username,
            role = admin.role,
        )

    def create_admin(
            self,
            data: CreateAdminRequest,
            admin_username: str,
            admin_password: str,
    ) -> CreateAdminResponse:

        current_admin = self.repository.find_by_username(admin_username)

        if current_admin is None:
            raise PermissionError("Invalid admin credentials")

        if not verify_password(
                admin_password,
                current_admin.password,
        ):
            raise PermissionError("Invalid admin credentials")

        if current_admin.role != Role.ADMIN:
            raise PermissionError("Only an admin can create another admin")

        if self.repository.find_by_username(data.username):
            raise ValueError("Username already exists")

        if self.repository.find_by_email(data.email):
            raise ValueError("Email already exists")

        admin = Admin(
            username=data.username,
            email=data.email,
            password=hash_password(data.password),
        )

        admin = self.repository.save_admin(admin)

        return CreateAdminResponse(
            id=admin.id,
            username=admin.username,
            email=admin.email,
            role=admin.role,
        )

    def delete_admin_by_username(
            self,
            username: str,
            admin_username: str,
            admin_password: str,
    ):
        current_admin = self.repository.find_by_username(admin_username)

        if current_admin is None:
            raise PermissionError("Invalid admin credentials")

        if not verify_password(
                admin_password,
                current_admin.password,
        ):
            raise PermissionError("Invalid admin credentials")

        if current_admin.role != Role.ADMIN:
            raise PermissionError("Only an admin can create another admin")

        if admin_username == username:
            raise ValueError("You cannot delete your own admin account while logged in")

        deleted_admin = self.repository.find_by_username(username)
        if not deleted_admin:
            raise ValueError(f"Admin with username '{username}' not found")
        self.repository.delete_admin(deleted_admin)
        return f"Admin with username '{username}' deleted"

