from app.config.state import AgentState
import json
from app.workflows.mail_assistant.agents.asset_request_handler import (
    AssetRequestHandlerAgent,
)
from app.services.chat_history import init_chat_history_service

chat_history_service = init_chat_history_service()


def asset_request_handler(state: AgentState):
    """Responsible for handling all the asset acquisition requests

    Args:
        state (AgentState): Memory for the agent ot refer from
    """
    response = AssetRequestHandlerAgent.asset_request_handler_agent.invoke(
        {"messages": [{"role": "user", "content": json.dumps(state)}]}
    )
    response_dict = json.loads(response["messages"][-1].content)
    print(response_dict)
    state["email_response"] = response_dict.get("email_response")
    state["ticket_message"] = response_dict.get("ticket_message")
    state["next"] = response_dict.get("next")
    state["messages"].append(response_dict.get("messages"))
    chat_history_service.add_llm_response(
        f"Asset Request Handler Agent: {response_dict.get("messages")}",
        state["thread_id"],
    )
    return state
