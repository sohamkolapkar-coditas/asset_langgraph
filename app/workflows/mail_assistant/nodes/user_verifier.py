from app.config.state import AgentState
from app.utils.email_check import check_email
from app.utils.constants.response_messages import ResponseMessages
from app.utils.user_check import check_user
from app.utils.constants.node_names import NodeNames


def user_verifier(state: AgentState):
    """
    Verifies the user based on the email address and user ID.

    Args:
        state (AgentState): The current state of the agent."""

    if not check_email(state.get("sender_email")):
        state["email_response"] = ResponseMessages.NON_ORG_EMAIL_MESSAGE.value
        state["next"] = NodeNames.EMAIL.value
        return state
    user_creds = check_user(state.get("sender_email"))
    if not user_creds:
        state["email_response"] = ResponseMessages.USER_NOT_IN_DB_MESSAGE.value
        state["next"] = NodeNames.EMAIL.value
        return state
    state["user_id"] = user_creds.get("id")
    state["next"] = NodeNames.THREAD_VERIFIER.value
    return state
