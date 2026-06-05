from langchain.tools import tool
from app.services.asset_item import init_asset_item_service
import uuid

asset_item_service = init_asset_item_service()


@tool
def check_asset(asset_category_id: str, location: str, asset_code: str):
    """This tool is used to check whether the asset exists in the database

    Args:
        asset_category_id (str): The category id of the asset (MUST be a UUID string, NOT an asset_code like "LP-1")
        location (str): The location of the asset
        asset_code (str): the code of the asset to be checked
    """
    # Validate that asset_category_id is a valid UUID format
    try:
        uuid.UUID(asset_category_id)
    except (ValueError, TypeError):
        raise ValueError(
            f"Invalid asset_category_id format: '{asset_category_id}'. "
            f"asset_category_id must be a valid UUID string (e.g., '9198f973-dfe3-40e0-8270-3e441cabd0dd'). "
            f"Asset codes like 'LP-1' are NOT valid. Please use the 'id' field from the check_category response."
        )

    item = asset_item_service.get_item(asset_code, asset_category_id, location)
    if item:
        return {
            "id": str(item.id),
            "name": item.name,
            "asset_code": item.asset_code,
            "asset_category_id": str(item.asset_category_id),
            "status": str(item.status),
            "location": item.location,
        }
    return "Asset not found with the provided details."
