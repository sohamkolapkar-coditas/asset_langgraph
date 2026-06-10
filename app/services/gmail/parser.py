import base64
import json
import os
import re

from email_reply_parser import EmailReplyParser

from app.config.state import AgentState
from app.services.gmail.auth import get_gmail_service
from app.workflows.mail_assistant.graph.builder import graph

HISTORY_ID_FILE = "last_history_id.txt"

# In-memory guard: prevents reprocessing the same msg_id within one process lifetime.
# Covers the race where two Pub/Sub retries arrive before the file is updated.
_processed_ids: set[str] = set()


def _load_history_id() -> str | None:
    if os.path.exists(HISTORY_ID_FILE):
        value = open(HISTORY_ID_FILE).read().strip()
        return value or None
    return None


def _save_history_id(history_id: str) -> None:
    with open(HISTORY_ID_FILE, "w") as f:
        f.write(history_id)


def parse_email_body(payload):
    """Recursively extracts and base64-decodes the text/plain part of an email."""
    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    body += base64.urlsafe_b64decode(data).decode("utf-8")
            elif "parts" in part:
                body += parse_email_body(part)
    elif "body" in payload:
        data = payload["body"].get("data")
        if data:
            body += base64.urlsafe_b64decode(data).decode("utf-8")
    return body


def process_gmail_update(data: dict):
    """
    Decodes the Pub/Sub push payload, fetches only NEW incoming messages via
    history.list, and invokes the LangGraph workflow for each one.

    Uses historyId tracking so outgoing replies (which also generate history
    events) are never mistaken for incoming emails.
    """
    service = get_gmail_service()

    pubsub_message = data.get("message", {})
    encoded_data = pubsub_message.get("data")
    if not encoded_data:
        print("No data in Pub/Sub message — skipping.")
        return

    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    json_data = json.loads(decoded_data)
    new_history_id = str(json_data.get("historyId", ""))
    print(f"\n--- Pub/Sub notification (historyId: {new_history_id}) ---")

    last_history_id = _load_history_id()
    if not last_history_id:
        # No baseline yet — save this ID and wait for the next notification.
        # Processing now would require fetching the full inbox which risks replays.
        print("No prior historyId on record — saving baseline, skipping this notification.")
        _save_history_id(new_history_id)
        return

    # Fetch history records for messages added to INBOX since last known ID.
    try:
        history_response = (
            service.users()
            .history()
            .list(
                userId="me",
                startHistoryId=last_history_id,
                historyTypes=["messageAdded"],
                labelId="INBOX",
            )
            .execute()
        )
    except Exception as exc:
        print(f"history.list failed: {exc} — advancing historyId to avoid replay.")
        _save_history_id(new_history_id)
        return

    # Advance the cursor BEFORE processing so a crash doesn't replay the same batch.
    _save_history_id(new_history_id)

    history_records = history_response.get("history", [])
    if not history_records:
        print("No new INBOX messages in this history window.")
        return

    # Collect unique message IDs that arrived in INBOX (excludes SENT/DRAFT).
    new_msg_ids: list[str] = []
    for record in history_records:
        for added in record.get("messagesAdded", []):
            msg_meta = added.get("message", {})
            msg_id = msg_meta.get("id")
            labels = msg_meta.get("labelIds", [])
            if msg_id and "INBOX" in labels and msg_id not in _processed_ids:
                new_msg_ids.append(msg_id)
                _processed_ids.add(msg_id)

    if not new_msg_ids:
        print("All messages in this batch were already processed or are not INBOX.")
        return

    for msg_id in new_msg_ids:
        print(f"Processing message {msg_id}")
        _process_single_message(service, msg_id)


def _process_single_message(service, msg_id: str):
    msg = service.users().messages().get(userId="me", id=msg_id).execute()
    payload = msg["payload"]
    headers = payload["headers"]

    state = AgentState()
    state["thread_id"] = msg.get("threadId")
    state["original_msg_id"] = next(
        (h["value"] for h in headers if h["name"] == "Message-ID"), ""
    )
    state["email_subject"] = next(
        (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
    )
    sender = next((h["value"] for h in headers if h["name"] == "From"), "")
    match = re.search(r"<(.+?)>", sender)
    state["sender_email"] = match.group(1) if match else sender.strip()

    email_text = parse_email_body(payload)
    state["email_body"] = EmailReplyParser.parse_reply(email_text).strip()

    return graph.invoke(state)
