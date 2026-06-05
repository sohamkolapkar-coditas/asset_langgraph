from sqlalchemy import Column, UUID, String, ForeignKey, Enum
from app.models.session import Base
from app.models.base import BaseClass
import uuid
from sqlalchemy.orm import relationship


class Software(Base, BaseClass):
    __tablename__ = "softwares"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    
