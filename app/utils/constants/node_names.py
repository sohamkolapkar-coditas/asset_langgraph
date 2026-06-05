from enum import Enum


class NodeNames(Enum):
    EMAIL = "email"
    THREAD_VERIFIER = "thread_verifier"
    ISSUE_HANDLER = "issue_handler"
    ASSET_REQUEST_HANDLER = "asset_request_handler"
    SOFTWARE_REQUEST_HANDLER = "software_request_handler"
