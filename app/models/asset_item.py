from sqlalchemy import Column, UUID, String, ForeignKey, Enum
from app.models.session import Base
from app.models.base import BaseClass
from app.utils.constants.asset_item import AssetItemStatus
import uuid
from sqlalchemy.orm import relationship


class AssetItem(Base, BaseClass):
    __tablename__ = "asset-items"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    asset_category_id = Column(UUID, ForeignKey("asset-categories.id"))
    asset_code = Column(String, nullable=False, unique=True)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    status = Column(
        Enum(AssetItemStatus), nullable=False, default=AssetItemStatus.AVAILABLE.value
    )
    location = Column(String, nullable=True)
    asset_category = relationship("AssetCategory", back_populates="items")
    user = relationship("User", back_populates="items")
