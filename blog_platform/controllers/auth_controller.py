from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from database import engine
from dependencies import get_session

from dtos.requests import RegisterRequest, LoginRequest
from services.auth_services import AuthService

from repositories.admin_repository import AdminRepository
from repositories.guest_repository import GuestRepository
from repositories.blogger_repository import BloggerRepository


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
    data: RegisterRequest,
    session: Session = Depends(get_session)
):
    auth_service = AuthService(
        AdminRepository(session),
        GuestRepository(session),
        BloggerRepository(session)
    )

    try:
        return auth_service.register(data)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))


@router.post("/login")
def login(
    data: LoginRequest,
    session: Session = Depends(get_session)
):
    auth_service = AuthService(
        AdminRepository(session),
        GuestRepository(session),
        BloggerRepository(session)
    )

    try:
        return auth_service.login(data)

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))