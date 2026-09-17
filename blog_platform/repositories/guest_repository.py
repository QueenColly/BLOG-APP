from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from models.guest import Guest


class GuestRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_guest(self, guest: Guest):
        self.session.add(guest)
        self.session.commit()
        self.session.refresh(guest)
        return guest

    def find_by_id(self, guest_id: UUID) -> Optional[Guest]:
        found_guest = select(Guest).where(Guest.id == guest_id)
        return self.session.exec(found_guest).first()

    def find_by_username(self, username: str) -> Optional[Guest]:
        found_username = select(Guest).where(Guest.username == username)
        return self.session.exec(found_username).first()


    def find_all(self) -> list[Guest]:
        all_guest = select(Guest)
        return list(self.session.exec(all_guest).all())

    def update_guest(self, guest: Guest) -> Guest:
        self.session.add(guest)
        self.session.commit()
        self.session.refresh(guest)
        return guest

    def find_by_email(self, email: str) -> Optional[Guest]:
        found_email = select(Guest).where(Guest.email == email)
        return self.session.exec(found_email).first()

    def delete_guest(self, guest: Guest) -> None:
        self.session.delete(guest)
        self.session.commit()





