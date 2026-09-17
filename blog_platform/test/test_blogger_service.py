import pytest
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

# Import ALL table models before create_all()
from models.blogger import Blogger
from models.post import Post, createPost, updatePost
from models.guest import Guest
from models.comment import Comment, createComment, updateComment


from repositories.blogger_repository import BloggerRepository
from repositories.post_repository import PostRepository
from repositories.comment_repository import CommentRepository

from services.blogger_service import BloggerService


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


class TestBloggerService:

    @pytest.fixture
    def session(self):
        SQLModel.metadata.create_all(engine)

        with Session(engine) as session:
            yield session

        SQLModel.metadata.drop_all(engine)

    @pytest.fixture
    def service(self, session):
        blogger_repository = BloggerRepository(session)
        post_repository = PostRepository(session)
        comment_repository = CommentRepository(session)

        return BloggerService(
            blogger_repository,
            post_repository,
            comment_repository,
        )

    def test_create_post(self, session, service):
        blogger = Blogger(
            username="blogger",
            email="blogger@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        data = createPost(
            title="My First Post",
            content="This is my first post",
            blogger_id=blogger.id,
        )

        post = service.create_post(data)

        assert post.title == "My First Post"
        assert post.content == "This is my first post"
        assert post.blogger_id == blogger.id

    def test_update_post(self, session, service):
        blogger = Blogger(
            username="blogger2",
            email="blogger2@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        post = Post(
            title="Old Title",
            content="Old Content",
            blogger_id=blogger.id,
        )

        session.add(post)
        session.commit()

        data = updatePost(
            title="New Title",
            content="New Content",
        )

        updated_post = service.update_post(
            post.id,
            blogger.id,
            data,
        )

        assert updated_post.title == "New Title"
        assert updated_post.content == "New Content"

    def test_delete_post(self, session, service):
        blogger = Blogger(
            username="blogger3",
            email="blogger3@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        post = Post(
            title="Post to Delete",
            content="Content",
            blogger_id=blogger.id,
        )

        session.add(post)
        session.commit()

        result = service.delete_post(
            post.id,
            blogger.id,
        )

        assert result == f"Post '{post.id}' deleted"

        found_post = session.get(Post, post.id)

        assert found_post is None

    def test_view_all_post(self, session, service):
        blogger = Blogger(
            username="blogger4",
            email="blogger4@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        post1 = Post(
            title="Post One",
            content="Content One",
            blogger_id=blogger.id,
        )

        post2 = Post(
            title="Post Two",
            content="Content Two",
            blogger_id=blogger.id,
        )

        session.add(post1)
        session.add(post2)
        session.commit()

        posts = service.view_all_post()

        assert len(posts) == 2

    def test_create_comment(self, session, service):
        blogger = Blogger(
            username="blogger5",
            email="blogger5@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        post = Post(
            title="My Post",
            content="Post Content",
            blogger_id=blogger.id,
        )

        session.add(post)
        session.commit()

        data = createComment(
            content="Nice post",
            post_id=post.id,
            blogger_id=blogger.id,
        )

        comment = service.create_comment(data)

        assert comment.content == "Nice post"
        assert comment.post_id == post.id
        assert comment.blogger_id == blogger.id

    def test_update_comment(self, session, service):
        blogger = Blogger(
            username="blogger6",
            email="blogger6@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        post = Post(
            title="My Post",
            content="Content",
            blogger_id=blogger.id,
        )

        session.add(post)
        session.commit()

        comment = Comment(
            content="Old Comment",
            post_id=post.id,
            blogger_id=blogger.id,
        )

        session.add(comment)
        session.commit()

        data = updateComment(
            content="New Comment",
        )

        updated_comment = service.update_comment(
            comment.id,
            blogger.id,
            data,
        )

        assert updated_comment.content == "New Comment"

    def test_delete_comment(self, session, service):
        blogger = Blogger(
            username="blogger7",
            email="blogger7@gmail.com",
            password="password",
        )

        session.add(blogger)
        session.commit()

        post = Post(
            title="My Post",
            content="Content",
            blogger_id=blogger.id,
        )

        session.add(post)
        session.commit()

        comment = Comment(
            content="Comment to delete",
            post_id=post.id,
            blogger_id=blogger.id,
        )

        session.add(comment)
        session.commit()

        result = service.delete_comment(
            comment.id,
            blogger.id,
        )

        assert result == f"Comment '{comment.id}' deleted"

        found_comment = session.get(Comment, comment.id)

        assert found_comment is None


