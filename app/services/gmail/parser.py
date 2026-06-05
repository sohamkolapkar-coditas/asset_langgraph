import base64
import json
from app.services.gmail.auth import get_gmail_service
from app.config.state import AgentState
from app.workflows.mail_assistant.graph.builder import graph

state = AgentState()


def parse_email_body(payload):
    """
    Recursively searches for the text/plain part of the email body
    and decodes it from base64.
    """
    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            # If it's a multipart, recurse deeper
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    body += base64.urlsafe_b64decode(data).decode("utf-8")
            elif "parts" in part:
                body += parse_email_body(part)
    elif "body" in payload:
        # If it's not multipart, the body is directly here
        data = payload["body"].get("data")
        if data:
            body += base64.urlsafe_b64decode(data).decode("utf-8")
    return body


def process_gmail_update(data: dict):
    """
    Decodes the Pub/Sub message and prints email details.
    """
    service = get_gmail_service()

    # 1. Decode the Pub/Sub message
    pubsub_message = data.get("message", {})
    encoded_data = pubsub_message.get("data")

    if not encoded_data:
        print("No data found in webhook.")
        return

    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    json_data = json.loads(decoded_data)
    print(json_data)
    # The historyId tells us a change occurred
    history_id = json_data.get("historyId")
    print(f"\n--- Update Received (History ID: {history_id}) ---")

    # 2. Fetch the latest email from the Inbox
    # We restrict this to 'INBOX' to avoid picking up Sent items or Drafts
    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], maxResults=1)
        .execute()
    )

    messages = results.get("messages", [])

    if not messages:
        print("No messages found in Inbox.")
        return

    # Get the specific message ID
    msg_id = messages[0]["id"]

    # 3. Get the full details of that message
    msg = service.users().messages().get(userId="me", id=msg_id).execute()
    payload = msg["payload"]
    headers = payload["headers"]
    state["thread_id"] = msg.get("threadId")
    # 4. Extract Metadata
    state["email_subject"] = next(
        (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
    )
    sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown")
    state["sender_email"] = sender[(sender.index("<")) + 1 : (sender.index(">"))]

    # 5. Extract Body
    email_text = parse_email_body(payload)
    deletion_text = email_text[email_text.find("\n") :]
    state["email_body"] = email_text.replace(deletion_text, " ")
    result = graph.invoke(state)
    return result
