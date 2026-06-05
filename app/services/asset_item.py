from typing import Annotated
from fastapi import Depends
from app.repository.asset_item import AssetItemRepository
from app.utils.init_repo import init_repo


class AssetItemService:

    def __init__(
        self,
        asset_item_repo: Annotated[
            AssetItemRepository, Depends(init_repo(class_name=AssetItemRepository))
        ],
    ):
        self.asset_item_repo = asset_item_repo

    def get_item(self, asset_code: str, asset_category_id: str, location: str):
        try:
            asset = self.asset_item_repo.get_asset_item(
                asset_code, asset_category_id, location
            )
            if not asset:
                return False
            return asset
        except Exception as e:
            raise e

    def get_user_assets(self, user_id: str, asset_category_id: str):
        try:
            items = self.asset_item_repo.get_user_assets(user_id, asset_category_id)
            if not items:
                return False
            return items

        except Exception as e:
            raise e

    def get_user_asset(self, asset_code: str, user_id: str):
        try:
            item = self.asset_item_repo.get_user_asset(user_id, asset_code)
            if not item:
                return False
            return item

        except Exception as e:
            raise e

    def get_asset(self, asset_category_id: str, location: str):
        try:
            items = self.asset_item_repo.get_asset(asset_category_id, location)
            if not items:
                return False
            return items

        except Exception as e:
            raise e


def init_asset_item_service():
    return AssetItemService(init_repo(class_name=AssetItemRepository))
