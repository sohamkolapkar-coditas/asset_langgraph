from sqlalchemy import Column, UUID, String, Integer
from app.models.session import Base
from app.models.base import BaseClass
import uuid
from sqlalchemy.orm import relationship


class AssetCategory(Base, BaseClass):
    __tablename__ = "asset-categories"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False, default=0)

    items = relationship("AssetItem", back_populates="asset_category")
