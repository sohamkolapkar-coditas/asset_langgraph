from enum import Enum


class ResponseMessages(Enum):
    USER_PROMPT_ADDED_SUCCESSFULLY = "User Prompt Added Successfully"
    LLM_RESPONSE_ADDED_SUCCESSFULLY = "LLM Response Added Successfully"
    TOOL_RESPONSE_ADDED_SUCCESSFULLY = "Tool Response Added Successfully"
    NON_ORG_EMAIL_MESSAGE = "User does not belong to the organization"
    USER_NOT_IN_DB_MESSAGE = "User has not been registered"
