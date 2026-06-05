from enum import Enum


class HttpConstants(Enum):
    HTTP_400_REQUEST = "Bad Request"

    # 404 Not Found
    HTTP_404_USER = "User Not Found"
    HTTP_404_ASSET_CATEGORY = "Asset Category Not Found"
    HTTP_404_ASSET_ITEM = "Asset Item Not Found"
    HTTP_404_SOFTWARE = "Software Not Found"

    # 401 Unauthorized Access
    HTTP_401_RESPONSE = "Invalid Credentials"

    # 403 Access Forbidden
    HTTP_403_RESPONSE = "Access Forbidden"

    # 409 Conflict
    HTTP_409_USER = "User Already Exists"
    HTTP_500_RESPONSE = "An Error has Occured"
