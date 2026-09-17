from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField


class createComment(BaseModel):
    content: str
    post_id: UUID
    blogger_id: Optional[UUID] = None
    guest_id: Optional[UUID] = None


class updateComment(BaseModel):
    content: Optional[str] = None


class Comment(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    content: str
    post_id: UUID = SQLField(foreign_key="post.id", index=True)
    blogger_id: Optional[UUID] = SQLField(default=None, foreign_key="blogger.id", index=True)
    guest_id: Optional[UUID] = SQLField(default=None, foreign_key="guest.id", index=True)
    created_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class CommentResponse(BaseModel):
    id: UUID
    content: str
    post_id: UUID
    blogger_id: Optional[UUID] = None
    guest_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

