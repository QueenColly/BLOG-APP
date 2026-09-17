
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field as SQLField
from models.user_role import Role


class createGuest(BaseModel):
    username: str
    email: str
    password: str

class updateGuest(BaseModel):
    username: Optional [str] = None
    email: Optional [str] = None
    password: Optional [str] = None

class Guest(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    username: str = SQLField(unique=True, index=True)
    email: EmailStr = SQLField(unique=True, index=True)
    role: Role = SQLField(default=Role.GUEST)
    created_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc))
    password: str

class GuestResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


