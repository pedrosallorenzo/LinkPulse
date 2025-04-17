from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from backend.database import Base
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
import uuid
from sqlalchemy.orm import relationship

class User(SQLAlchemyBaseUserTableUUID, Base):
    links = relationship("Link", backref="user")

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    user_id = Column(ForeignKey("user.id"))
    is_online = Column(Boolean, default=True)