from sqlalchemy import Column, UUID, String, ForeignKey, Enum
from app.models.session import Base
from app.models.base import BaseClass
import uuid
from sqlalchemy.orm import relationship


class ChatHistory(Base, BaseClass):
    __tablename__ = "chat-histories"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    thread_id = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"))
    role = Column(String, nullable=False)
    message = Column(String, nullable=True)

    user = relationship("User", back_populates="chat_history")
