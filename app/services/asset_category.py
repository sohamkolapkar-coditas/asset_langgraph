from typing import Annotated
from fastapi import Depends
from app.repository.asset_category import AssetCategoryRepository
from app.utils.init_repo import init_repo


class AssetCategoryService:

    def __init__(
        self,
        asset_category_repo: Annotated[
            AssetCategoryRepository,
            Depends(init_repo(class_name=AssetCategoryRepository)),
        ],
    ):
        self.asset_category_repo = asset_category_repo

    def get_asset_category(self, category_name: str):
        try:
            category = self.asset_category_repo.get_category(category_name)
            if not category:
                return False
            return category
        except Exception as e:
            raise e

    def get_categories(self):
        try:
            categories = self.asset_category_repo.get_categories()
            if not categories:
                return False
            return categories
        except Exception as e:
            raise e


def init_asset_category_service():
    return AssetCategoryService(init_repo(class_name=AssetCategoryRepository))
