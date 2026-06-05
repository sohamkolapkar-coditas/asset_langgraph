from sqlalchemy import Column, UUID, String
from app.models.session import Base
from app.models.base import BaseClass
import uuid
from sqlalchemy.orm import relationship


class User(Base, BaseClass):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)

    chat_history = relationship("ChatHistory", back_populates="user")
    items = relationship("AssetItem", back_populates="user")
