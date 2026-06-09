from app.services.gmail.auth import get_gmail_service
from email.mime.text import MIMEText
import base64
from app.config.state import AgentState


def send_email(state: AgentState):
    service = get_gmail_service()
    message = MIMEText(state["email_response"])
    message["to"] = state["sender_email"]
    message["subject"] = f"Re: {state['email_subject']}"
    message["In-Reply-To"] = state["original_msg_id"]
    message["References"] = state["original_msg_id"]

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    body = {"raw": raw_message, "thread_id": state["thread_id"]}

    service.users().messages().send(userId="me", body=body).execute()
    return state
