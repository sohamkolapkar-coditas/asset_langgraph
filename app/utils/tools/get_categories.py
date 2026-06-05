from langchain.tools import tool
from app.services.asset_category import (
    init_asset_category_service,
)
from app.utils.constants.http_response import HttpConstants

asset_category_service = init_asset_category_service()


@tool
def get_categories():
    """This tool is used to retrieve all the existing asset categories from the database."""
    categories = asset_category_service.get_categories()
    if categories:
        return categories
    return HttpConstants.HTTP_404_ASSET_CATEGORY.value