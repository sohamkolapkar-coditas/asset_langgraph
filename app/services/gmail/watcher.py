from app.services.gmail.auth import get_gmail_service


def watch_gmail():
    service = get_gmail_service()
    
    # Replace this with your full topic name from Google Cloud Console
    # Format: projects/{project_id}/topics/{topic_name}
    TOPIC_NAME = "projects/gmail-assistant-481910/topics/gmail-topic"

    request = {
        'labelIds': ['INBOX'],  # Only notify for Inbox changes
        'topicName': TOPIC_NAME
    }
    
    # Execute the watch
    response = service.users().watch(userId='me', body=request).execute()
    print("Watch setup successful:", response)

    # Persist the starting historyId so process_gmail_update has a baseline.
    history_id = response.get("historyId")
    if history_id:
        with open("last_history_id.txt", "w") as f:
            f.write(str(history_id))
        print(f"Saved baseline historyId: {history_id}")

if __name__ == '__main__':
    watch_gmail()