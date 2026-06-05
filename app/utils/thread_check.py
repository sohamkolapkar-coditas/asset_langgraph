from app.services.chat_history import init_chat_history_service

chat_history_service = init_chat_history_service()


def check_thread_exists(
    thread_id: str,
):
    """This tool is used to check if the thread is already in the database confirming if this is a new conversation or an continued conversation.
    If the thread is already in the database it returns the conversation history.

    Args:
        thread_id (str): The id of the thread of the email
    """
    thread = chat_history_service.get_chat_history(thread_id)
    if thread:
        return thread
    return False
