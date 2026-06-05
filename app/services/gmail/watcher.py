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

if __name__ == '__main__':
    watch_gmail()