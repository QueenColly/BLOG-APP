from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from models.post import Post


class PostRepository:

    def __init__(self, session: Session):
        self.session = session

    def save_post(self, post: Post) -> Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def find_by_id(self, post_id: UUID) -> Optional[Post]:
        statement = select(Post).where(Post.id == post_id)
        return self.session.exec(statement).first()

    def find_all(self) -> list[Post]:
        statement = select(Post)
        return list(self.session.exec(statement).all())

    def update_post(self, post: Post) -> Post:
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete_post(self, post: Post) -> None:
        self.session.delete(post)
        self.session.commit()