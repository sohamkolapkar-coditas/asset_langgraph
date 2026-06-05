from app.models.asset_categories import AssetCategory
from sqlalchemy.orm import Session
from app.utils.constants.error_messages import ErrorMessages


class AssetCategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_category(self, category_name: str):
        try:
            category = (
                self.db.query(AssetCategory)
                .filter(AssetCategory.name == category_name)
                .first()
            )
            return category

        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def get_categories(self):
        try:
            categories = (
                self.db.query(AssetCategory).filter(AssetCategory.is_active).all()
            )
            return categories

        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)
