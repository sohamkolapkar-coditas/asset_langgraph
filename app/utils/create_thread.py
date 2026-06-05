from app.services.chat_history import init_chat_history_service

chat_history_service = init_chat_history_service()


def create_thread(
    thread_id: str,
    user_query: str,
):
    """This tool is used to create a new conversation in the database.

    Args:
        thread_id (str): The thread_id of the email
        user_query (str): The body of the email entered by user

    """
    response = chat_history_service.add_user_prompt(user_query, thread_id)
    return response
