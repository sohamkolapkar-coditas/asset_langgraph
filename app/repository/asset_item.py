from app.models.asset_item import AssetItem
from sqlalchemy.orm import Session
from app.utils.constants.error_messages import ErrorMessages
from sqlalchemy import and_
from app.utils.constants.asset_item import AssetItemStatus


class AssetItemRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_asset_item(self, asset_code: str, asset_category_id: str, location: str):
        try:
            if asset_code:
                item = (
                    self.db.query(AssetItem)
                    .filter(
                        and_(
                            AssetItem.asset_code == asset_code,
                            AssetItem.asset_category_id == asset_category_id,
                            AssetItem.status == AssetItemStatus.AVAILABLE.value,
                            AssetItem.location == location,
                        )
                    )
                    .first()
                )
                return item
            item = (
                self.db.query(AssetItem)
                .filter(
                    and_(
                        AssetItem.asset_category_id == asset_category_id,
                        AssetItem.status == AssetItemStatus.AVAILABLE.value,
                        AssetItem.location == location,
                    )
                )
                .first()
            )
            return item
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def get_user_assets(self, user_id: str, asset_category_id: str):
        try:
            items = (
                self.db.query(AssetItem)
                .filter(
                    and_(
                        AssetItem.user_id == user_id,
                        AssetItem.asset_category_id == asset_category_id,
                    )
                )
                .all()
            )
            return items
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def get_user_asset(self, user_id: str, asset_code: str):
        try:
            item = (
                self.db.query(AssetItem)
                .filter(
                    and_(
                        AssetItem.user_id == user_id,
                        AssetItem.asset_code == asset_code,
                        AssetItem.is_active,
                    )
                )
                .first()
            )
            return item
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def get_asset(self, asset_category_id: str, location: str):
        try:
            item = (
                self.db.query(AssetItem)
                .filter(
                    and_(
                        AssetItem.asset_category_id == asset_category_id,
                        AssetItem.location == location,
                        AssetItem.is_active,
                        AssetItem.status == AssetItemStatus.AVAILABLE.value,
                    )
                )
                .all()
            )
            return item
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)
