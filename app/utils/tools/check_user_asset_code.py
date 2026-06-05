from langchain.tools import tool
from app.services.asset_item import init_asset_item_service

asset_item_service = init_asset_item_service()


@tool
def check_user_asset_code(asset_code: str, user_id: str):
    """This tool is used to check if the user has that specific asset

    Args:
        asset_code (str): the code of the asset to be checked
        user_id (str): the user_id of the user
    """

    item = asset_item_service.get_user_asset(asset_code, user_id)
    if item:
        return {
            "id": str(item.id),
            "name": item.name,
            "asset_code": item.asset_code,
            "asset_category_id": str(item.asset_category_id),
            "status": str(item.status),
            "location": item.location,
        }
    return "Asset code verification failed. No matching asset found for this user."
