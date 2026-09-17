
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField


class createPost(BaseModel):
    title: str
    content: str
    blogger_id: UUID


class updatePost(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class Post(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    title: str = SQLField(index=True)
    content: str
    blogger_id: UUID = SQLField(foreign_key="blogger.id", index=True)
    created_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc)
    )

class PostResponse(BaseModel):
    id: UUID
    title: str
    content: str
    blogger_id: UUID
    created_at : datetime

    class Config:
        from_attributes = True
