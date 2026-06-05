from app.config.state import AgentState
from app.services.chat_history import init_chat_history_service
from app.utils.thread_check import check_thread_exists
from app.utils.create_thread import create_thread

chat_history_service = init_chat_history_service()


def thread_verifier(state: AgentState):
    """Verifies if the recieved email is a new conversation or existing one by checking it in the database.

    Args:
        state (AgentState): Memory for the agents to refer from
    """
    chat_history_service.add_user_prompt(
        f"Email Subject: {state.get("email_subject")} \n Email Body: {state.get("email_body")}",
        state.get("thread_id"),
    )

    thread = check_thread_exists(state.get("thread_id"))
    if not thread:
        response = create_thread(
            state.get("thread_id"),
            f"Email Subject: {state.get("email_subject")} \n Email Body: {state.get("email_body")}",
        )
        if not state.get("messages"):
            state["messages"] = [response]
        else:
            state["messages"].append(response)
        return state
    state["messages"] = []
    state["chat_history"] = thread
    return state
