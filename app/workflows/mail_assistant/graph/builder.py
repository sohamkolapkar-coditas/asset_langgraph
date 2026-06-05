from langgraph.graph import StateGraph, END, START
from app.config.state import AgentState
from app.workflows.mail_assistant.nodes.asset_request_handler import (
    asset_request_handler,
)
from app.workflows.mail_assistant.nodes.email import send_email
from app.workflows.mail_assistant.nodes.software_request_handler import (
    software_request_handler,
)
from app.workflows.mail_assistant.nodes.supervisor import supervisor
from app.workflows.mail_assistant.nodes.issue_handler import issue_handler
from app.workflows.mail_assistant.nodes.thread_verifier import thread_verifier
from app.workflows.mail_assistant.nodes.user_verifier import user_verifier
from app.workflows.mail_assistant.nodes.ticket_generator import ticket_generator

workflow = StateGraph(AgentState)
workflow.add_node("email", send_email)
workflow.add_node("thread_verifier", thread_verifier)
workflow.add_node("user_verifier", user_verifier)
workflow.add_node("issue_handler", issue_handler)
workflow.add_node("software_request_handler", software_request_handler)
workflow.add_node("asset_request_handler", asset_request_handler)
workflow.add_node("ticket_generator", ticket_generator)
workflow.add_node("supervisor", supervisor)

workflow.add_edge(START, "user_verifier")


def choose_next_node(state: AgentState):
    return state["next"]


workflow.add_conditional_edges(
    "user_verifier",
    choose_next_node,
    {"thread_verifier": "thread_verifier", "email": "email"},
)
workflow.add_edge("thread_verifier", "supervisor")
workflow.add_conditional_edges(
    "supervisor",
    choose_next_node,
    {
        "issue_handler": "issue_handler",
        "software_request_handler": "software_request_handler",
        "asset_request_handler": "asset_request_handler",
        "email": "email",
        "ticket_generator": "ticket_generator",
    },
)

workflow.add_edge("issue_handler", "supervisor")
workflow.add_edge("software_request_handler", "supervisor")
workflow.add_edge("asset_request_handler", "supervisor")
workflow.add_edge("ticket_generator", "supervisor")
workflow.add_edge("email", END)

graph = workflow.compile()
