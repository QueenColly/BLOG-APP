from sqlmodel import SQLModel, create_engine
from urllib.parse import quote_plus

engine = create_engine(
    f"mysql+pymysql://user1:"
    f"{quote_plus('password')}"
    f"@localhost:3306/blog_platform"
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)