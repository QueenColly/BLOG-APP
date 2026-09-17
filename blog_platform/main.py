from fastapi import FastAPI
from database import create_db_and_tables
from contextlib import asynccontextmanager
from controllers.admin_controller import router as admin_router
from controllers.blogger_controller import router as blogger_router
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from models.admin import Admin
from models.blogger import Blogger
from models.guest import Guest
from models.post import Post
from models.comment import Comment



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(blogger_router)
app.include_router(auth_router)