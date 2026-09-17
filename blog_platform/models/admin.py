from datetime import datetime, timezone
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel ,Field as SQLField
from models.user_role import Role



class Admin(SQLModel, table=True):
    id: UUID = SQLField(default_factory=uuid4, primary_key=True)
    username: str = SQLField(unique=True, index=True)
    email: EmailStr = SQLField(unique=True, index=True)
    role: Role = SQLField(default=Role.ADMIN)
    created_at: datetime = SQLField(
        default_factory=lambda: datetime.now(timezone.utc))
    password: str




