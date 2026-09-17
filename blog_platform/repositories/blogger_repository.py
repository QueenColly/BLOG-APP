from typing import Optional
from uuid import UUID
from sqlmodel import Session, select
from models.blogger import Blogger


class BloggerRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_blogger(self, blogger: Blogger):
        self.session.add(blogger)
        self.session.commit()
        self.session.refresh(blogger)
        return blogger

    def find_by_id(self, blogger_id: UUID) -> Optional[Blogger]:
        found_blogger = select(Blogger).where(Blogger.id == blogger_id)
        return self.session.exec(found_blogger).first()

    def find_by_username(self, username: str) -> Optional[Blogger]:
        found_username = select(Blogger).where(Blogger.username == username)
        return self.session.exec(found_username).first()


    def find_all(self) -> list[Blogger]:
        all_blogger = select(Blogger)
        return list(self.session.exec(all_blogger).all())

    def update_blogger(self, blogger: Blogger) -> Blogger:
        self.session.add(blogger)
        self.session.commit()
        self.session.refresh(blogger)
        return blogger

    def find_by_email(self, email: str) -> Optional[Blogger]:
        found_email = select(Blogger).where(Blogger.email == email)
        return self.session.exec(found_email).first()

    def delete_blogger(self, blogger: Blogger) -> None:
        self.session.delete(blogger)
        self.session.commit()





