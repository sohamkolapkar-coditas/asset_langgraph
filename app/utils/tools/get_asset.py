from langchain.tools import tool
from app.services.asset_item import init_asset_item_service
import uuid

asset_item_service = init_asset_item_service()


@tool
def get_asset(asset_category_id: str, location: str):
    """This tool is used check whether the asset exists in the specified location

    Args:
        asset_category_id (str): The category id of the asset (MUST be a UUID string, NOT an asset_code like "LP-1")
        location (str): The location of the asset
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

    items = asset_item_service.get_asset(asset_category_id, location)
    if items:
        if len(items) == 1:
            return items
        elif len(items) > 1:
            items = [item.__dict__ for item in items]
            return items
    return "Asset not found in the specified location."
