from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from models.comment import Comment


class CommentRepository:

    def __init__(self, session: Session):
        self.session = session

    def save_comment(self, comment: Comment) -> Comment:
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def find_by_id(self, comment_id: UUID) -> Optional[Comment]:
        statement = select(Comment).where(Comment.id == comment_id)
        return self.session.exec(statement).first()

    def update_comment(self, comment: Comment) -> Comment:
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def delete_comment(self, comment: Comment) -> None:
        self.session.delete(comment)
        self.session.commit()