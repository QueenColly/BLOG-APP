from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from models.admin import Admin


class AdminRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_admin(self, admin: Admin):
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin

    def find_by_id(self, admin_id: UUID) -> Optional[Admin]:
        found_admin = select(Admin).where(Admin.id == admin_id)
        return self.session.exec(found_admin).first()

    def find_by_username(self, username: str) -> Optional[Admin]:
        found_username = select(Admin).where(Admin.username == username)
        return self.session.exec(found_username).first()


    def find_all(self) -> list[Admin]:
        all_admin = select(Admin)
        return list(self.session.exec(all_admin).all())

    def update_admin(self, admin: Admin) -> Admin:
        self.session.add(admin)
        self.session.commit()
        self.session.refresh(admin)
        return admin

    def find_by_email(self, email: str) -> Optional[Admin]:
        found_email = select(Admin).where(Admin.email == email)
        return self.session.exec(found_email).first()

    def delete_admin(self, admin: Admin) -> None:
        self.session.delete(admin)
        self.session.commit()





