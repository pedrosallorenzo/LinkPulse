from fastapi_users import FastAPIUsers, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.authentication import CookieTransport, AuthenticationBackend, BearerTransport, JWTStrategy
from backend.models import User
from backend.database import SessionLocal
import uuid
import os
from fastapi_users import schemas

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass

class UserCreate(schemas.BaseUserCreate):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass

SECRET = os.getenv("SECRET", "SUPERSECRET")

cookie_transport = CookieTransport(cookie_name="linkpulse", cookie_secure=False)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

db = SessionLocal()
user_db = SQLAlchemyUserDatabase(User, db)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    user_db,
    [auth_backend],
    User,
    UserCreate,
    UserUpdate,
    UserRead,
)

current_active_user = fastapi_users.current_user(active=True)