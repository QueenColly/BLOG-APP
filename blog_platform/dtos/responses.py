import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr
from models.user_role import Role

class RegisterResponse(BaseModel):
    id : UUID
    email : EmailStr
    username: str
    role: Role

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    id : UUID
    username : str
    role : Role

    class Config:
        from_attributes = True

class CreateAdminResponse(BaseModel):
    id : UUID
    email : EmailStr
    username: str
    role: Role

    class Config:
        from_attributes = True

class BloggerResponse(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
