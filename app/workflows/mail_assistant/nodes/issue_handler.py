from app.config.state import AgentState
import json
from app.workflows.mail_assistant.agents.issue_handler import IssueHandlerAgent
from app.services.chat_history import init_chat_history_service

chat_history_service = init_chat_history_service()


def issue_handler(state: AgentState):
    """Responsible for handling all the issues of the assets.

    Args:
        state (AgentState): Memory for the agent to refer from
    """

    response = IssueHandlerAgent.issue_handler_agent.invoke(
        {"messages": [{"role": "user", "content": json.dumps(state)}]}
    )
    response_dict = json.loads(response["messages"][-1].content)
    print(response_dict)
    state["email_response"] = response_dict.get("email_response")
    state["ticket_message"] = response_dict.get("ticket_message")
    state["next"] = response_dict.get("next")
    state["messages"].append(response_dict.get("messages"))
    chat_history_service.add_llm_response(
        f"Issue Handler Agent: {response_dict.get("messages")}", state["thread_id"]
    )
    return state
