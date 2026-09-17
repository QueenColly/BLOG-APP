from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from dependencies import get_session
from dtos.requests import CreateAdminRequest
from dtos.responses import CreateAdminResponse
from repositories.admin_repository import AdminRepository
from services.admin_service import AdminService

router = APIRouter(
    prefix="/admins",
    tags=["Admin"],
)

def get_admin_service(session: Session = Depends(get_session)) -> AdminService:
    repository = AdminRepository(session)
    return AdminService(repository)


@router.post(
    "/first",
    response_model=CreateAdminResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_first_admin(
    data: CreateAdminRequest,
    service: AdminService = Depends(get_admin_service),
):
    try:
        return service.create_first_admin(data)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@router.post(
    "/create",
    response_model=CreateAdminResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_admin(
    data: CreateAdminRequest,
    admin_username: str,
    admin_password: str,
    service: AdminService = Depends(get_admin_service),
):
    try:
        return service.create_admin(
            data=data,
            admin_username=admin_username,
            admin_password=admin_password,
        )
    except PermissionError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )


@router.delete(
    "/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_admin(
    username: str,
    admin_username: str,
    admin_password: str,
    service: AdminService = Depends(get_admin_service),
):
    try:
        service.delete_admin_by_username(
            username=username,
            admin_username=admin_username,
            admin_password=admin_password,
        )
        return f"Admin with username '{username}' deleted"
    except PermissionError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(err),
        )
    except ValueError as err:
        if "not found" in str(err).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(err),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )