import json
import time

from langchain_core.messages import HumanMessage, SystemMessage

from app.config.inference import llm_model
from app.config.state import AgentState
from app.services.chat_history import init_chat_history_service
from app.utils.llm_utils import parse_llm_json
from app.workflows.mail_assistant.prompts.supervisor import SUPERVISOR_PROMPT

chat_history_service = init_chat_history_service()

MAX_RETRIES = 3


def supervisor(state: AgentState):
    """Responsible for planning and supervising the functioning

    Args:
        state (AgentState): Memory for the agent to refer from
    """
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = llm_model.invoke([
                SystemMessage(content=SUPERVISOR_PROMPT),
                HumanMessage(content=json.dumps(state)),
            ])
            response_dict = parse_llm_json(response.content)
            break
        except (ValueError, json.JSONDecodeError) as e:
            last_error = e
            if attempt < MAX_RETRIES:
                time.sleep(1)
    else:
        raise RuntimeError(
            f"Supervisor LLM failed to return valid JSON after {MAX_RETRIES} attempts: {last_error}"
        ) from last_error

    state["plan"] = response_dict.get("plan")
    print(state["plan"])
    state["next"] = response_dict.get("next")
    if response_dict.get("email_response"):
        state["email_response"] = response_dict.get("email_response")

    # Hard override: if any handler or ticket_generator left a non-empty email_response
    # in state, the only valid next hop is "email" — enforce it regardless of LLM output.
    if state.get("email_response"):
        state["next"] = "email"

    chat_history_service.add_llm_response(
        f"Supervisor Agent: {response_dict.get('plan')}",
        state["thread_id"],
    )
    return state
