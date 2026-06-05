from typing_extensions import TypedDict
from typing import Any


class AgentState(TypedDict):
    email_subject: str
    plan: str
    location: str
    user_id: str
    sender_email: str
    thread_id: str
    original_msg_id: str
    chat_history: list[Any]
    messages: list[Any]
    next: str
    email_response: str
    ticket_message: str
    email_body: str
