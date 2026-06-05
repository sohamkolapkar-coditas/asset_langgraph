from enum import Enum


class AssetItemStatus(Enum):
    AVAILABLE = "AVAILABLE"
    ALLOCATED = "ALLOCATED"
    RETIRED = "RETIRED"


class AssetItemLocation(Enum):
    NYATI = "NYATI"
    GAIA = "GAIA"
