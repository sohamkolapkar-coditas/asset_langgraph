from langchain.tools import tool
from app.services.asset_item import init_asset_item_service
import uuid

asset_item_service = init_asset_item_service()


@tool
def user_asset(user_id: str, asset_category_id: str):
    """This tool is used to get all the assets of the user

    Args:
        user_id (str): The id of the user
        asset_category_id (str): The id of the asset category (MUST be a UUID string, NOT an asset_code like "LP-1")
    """
    # Validate that asset_category_id is a valid UUID format
    try:
        print("User asset tool")
        uuid.UUID(asset_category_id)
    except (ValueError, TypeError):
        raise ValueError(
            f"Invalid asset_category_id format: '{asset_category_id}'. "
            f"asset_category_id must be a valid UUID string (e.g., '9198f973-dfe3-40e0-8270-3e441cabd0dd'). "
            f"Asset codes like 'LP-1' are NOT valid. Please use the 'id' field from the check_category response."
        )

    items = asset_item_service.get_user_assets(user_id, asset_category_id)
    if not items:
        return "No assets found for this user in the specified category."
    item_list = []
    for item in items:
        item_list.append(
            {
                "id": str(item.id),
                "name": item.name,
                "asset_category_id": str(item.asset_category_id),
                "asset_code": item.asset_code,
                "status": str(item.status),
                "location": item.location,
            }
        )
    return item_list
