from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from dependencies import get_session

from dtos.responses import BloggerResponse

from models.blogger import CreateBlogger, UpdateBlogger
from models.post import createPost, updatePost
from models.comment import createComment, updateComment

from repositories.blogger_repository import BloggerRepository
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository

from services.blogger_service import BloggerService


router = APIRouter(
    prefix="/bloggers",
    tags=["Blogger"],
)


def get_blogger_service(
    session: Session = Depends(get_session),
) -> BloggerService:

    blogger_repository = BloggerRepository(session)
    post_repository = PostRepository(session)
    comment_repository = CommentRepository(session)

    return BloggerService(
        blogger_repository=blogger_repository,
        post_repository=post_repository,
        comment_repository=comment_repository,
    )

@router.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
)
def create_post(
    data: createPost,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return service.create_post(data)

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )
@router.get(
    "/posts",
)
def view_all_post(
    service: BloggerService = Depends(get_blogger_service),
):
    return service.view_all_post()


@router.put(
    "/posts/{post_id}",
)
def update_post(
    post_id: UUID,
    blogger_id: UUID,
    data: updatePost,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return service.update_post(
            post_id=post_id,
            blogger_id=blogger_id,
            data=data,
        )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )

    except PermissionError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(err),
        )


@router.delete(
    "/posts/{post_id}",
)
def delete_post(
    post_id: UUID,
    blogger_id: UUID,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        service.delete_post(
            post_id=post_id,
            blogger_id=blogger_id,
        )

        return {
            "message": f"Post '{post_id}' deleted successfully"
        }

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )

    except PermissionError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(err),
        )

@router.post(
    "/comments",
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    data: createComment,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return service.create_comment(data)

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )


@router.put(
    "/comments/{comment_id}",
)
def update_comment(
    comment_id: UUID,
    blogger_id: UUID,
    data: updateComment,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return service.update_comment(
            comment_id=comment_id,
            blogger_id=blogger_id,
            data=data,
        )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )

    except PermissionError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(err),
        )


@router.delete(
    "/comments/{comment_id}",
)
def delete_comment(
    comment_id: UUID,
    blogger_id: UUID,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        service.delete_comment(
            comment_id=comment_id,
            blogger_id=blogger_id,
        )

        return {
            "message": f"Comment '{comment_id}' deleted successfully"
        }

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )

    except PermissionError as err:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(err),
        )

@router.post(
    "",
    response_model=BloggerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_blogger(
    data: CreateBlogger,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return service.create_blogger(data)

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        )

@router.get(
    "",
    response_model=list[BloggerResponse],
)
def view_all_bloggers(
    service: BloggerService = Depends(get_blogger_service),
):
    return service.view_all_bloggers()

@router.put(
    "/{blogger_id}",
    response_model=BloggerResponse,
)
def update_blogger(
    blogger_id: UUID,
    data: UpdateBlogger,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return service.update_blogger(
            blogger_id=blogger_id,
            data=data,
        )

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )


@router.delete(
    "/{blogger_id}",
)
def delete_blogger(
    blogger_id: UUID,
    service: BloggerService = Depends(get_blogger_service),
):
    try:
        return {
            "message": service.delete_blogger(blogger_id)
        }

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err),
        )



