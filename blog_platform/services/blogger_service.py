from uuid import UUID

from models.blogger import CreateBlogger, Blogger, CreateBlogger, UpdateBlogger
from models.post import Post, createPost, updatePost
from models.comment import Comment, createComment, updateComment

from repositories.blogger_repository import BloggerRepository
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository


class BloggerService:

    def __init__(
        self,
        blogger_repository: BloggerRepository,
        post_repository: PostRepository,
        comment_repository: CommentRepository,
    ):
        self.blogger_repository = blogger_repository
        self.post_repository = post_repository
        self.comment_repository = comment_repository

    def create_blogger(self, data: CreateBlogger):

        existing_username = self.blogger_repository.find_by_username(
            data.username
        )

        if existing_username:
            raise ValueError("Username already exists")

        existing_email = self.blogger_repository.find_by_email(
            data.email
        )

        if existing_email:
            raise ValueError("Email already exists")

        blogger = Blogger(
            username=data.username,
            email=data.email,
            password=data.password,
        )

        return self.blogger_repository.save_blogger(blogger)

    def view_blogger(self, blogger_id: UUID):

        blogger = self.blogger_repository.find_by_id(blogger_id)

        if blogger is None:
            raise ValueError("Blogger not found")

        return blogger

    def view_all_bloggers(self):

        return self.blogger_repository.find_all()

    def update_blogger(
            self,
            blogger_id: UUID,
            data: UpdateBlogger,
    ):

        blogger = self.blogger_repository.find_by_id(blogger_id)

        if blogger is None:
            raise ValueError("Blogger not found")

        if data.username is not None:
            blogger.username = data.username

        if data.email is not None:
            blogger.email = data.email

        if data.password is not None:
            blogger.password = data.password

        return self.blogger_repository.update_blogger(blogger)

    def delete_blogger(self, blogger_id: UUID):

        blogger = self.blogger_repository.find_by_id(blogger_id)

        if blogger is None:
            raise ValueError("Blogger not found")

        self.blogger_repository.delete_blogger(blogger)

        return f"Blogger '{blogger_id}' deleted successfully"


    def create_post(self, data: createPost):

        blogger = self.blogger_repository.find_by_id(
            data.blogger_id
        )

        if blogger is None:
            raise ValueError("Blogger not found")

        post = Post(
            title=data.title,
            content=data.content,
            blogger_id=data.blogger_id,
        )

        return self.post_repository.save_post(post)

    def update_post(
        self,
        post_id: UUID,
        blogger_id: UUID,
        data: updatePost,
    ):

        post = self.post_repository.find_by_id(post_id)

        if post is None:
            raise ValueError("Post not found")

        if post.blogger_id != blogger_id:
            raise PermissionError(
                "You can only update your own post"
            )

        if data.title is not None:
            post.title = data.title

        if data.content is not None:
            post.content = data.content

        return self.post_repository.update_post(post)

    def delete_post(
        self,
        post_id: UUID,
        blogger_id: UUID,
    ):

        post = self.post_repository.find_by_id(post_id)

        if post is None:
            raise ValueError("Post not found")

        if post.blogger_id != blogger_id:
            raise PermissionError(
                "You can only delete your own post"
            )

        self.post_repository.delete_post(post)

        return f"Post '{post_id}' deleted"

    def view_all_post(self):

        return self.post_repository.find_all()

    # COMMENT METHODS

    def create_comment(self, data: createComment):

        post = self.post_repository.find_by_id(
            data.post_id
        )

        if post is None:
            raise ValueError("Post not found")

        comment = Comment(
            content=data.content,
            post_id=data.post_id,
            blogger_id=data.blogger_id,
            guest_id=data.guest_id,
        )

        return self.comment_repository.save_comment(comment)

    def update_comment(
        self,
        comment_id: UUID,
        blogger_id: UUID,
        data: updateComment,
    ):

        comment = self.comment_repository.find_by_id(
            comment_id
        )

        if comment is None:
            raise ValueError("Comment not found")

        if comment.blogger_id != blogger_id:
            raise PermissionError(
                "You can only update your own comment"
            )

        if data.content is not None:
            comment.content = data.content

        return self.comment_repository.update_comment(comment)

    def delete_comment(
        self,
        comment_id: UUID,
        blogger_id: UUID,
    ):

        comment = self.comment_repository.find_by_id(
            comment_id
        )

        if comment is None:
            raise ValueError("Comment not found")

        if comment.blogger_id != blogger_id:
            raise PermissionError(
                "You can only delete your own comment"
            )

        self.comment_repository.delete_comment(comment)

        return f"Comment '{comment_id}' deleted"