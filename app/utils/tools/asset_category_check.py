from langchain.tools import tool
from app.services.asset_category import (
    init_asset_category_service,
)

asset_category_service = init_asset_category_service()


@tool
def check_category(
    name: str,
):
    """This tool is used to check if the asset category exists in database

    Args:
        name (str): name of the category
    """
    print("Check Category tool")
    category = asset_category_service.get_asset_category(name)
    if category:
        return {
            "id": str(category.id),
            "name": category.name,
            "quantity": category.quantity,
        }
    return "Category not found in the database."
