from fastapi import APIRouter
from app.config.state import AgentState

state = AgentState()
mock_router = APIRouter(prefix="/mock")
from app.workflows.mail_assistant.graph.builder import graph


@mock_router.post("/asset-request")
async def asset_request_mock():
    state["thread_id"] = "2"
    state["email_subject"] = "I want a new laptop"
    state["sender_email"] = "soham.kolapkar@coditas.com"
    state["email_body"] = "I want a new laptop"
    result = graph.invoke(state)
    return result


@mock_router.post("/issue-handling")
async def issue_handler_mock():
    state["thread_id"] = "456789"
    state["email_subject"] = "My laptop is not working"
    state["sender_email"] = "soham.kolapkar@coditas.com"
    state["email_body"] = "My laptop is not working"
    result = graph.invoke(state)
    return result


@mock_router.post("/software-request")
async def software_request_mock():
    state["thread_id"] = "098764"
    state["email_subject"] = "I want Cursor on my laptop"
    state["sender_email"] = "soham.kolapkar@coditas.com"
    state["email_body"] = "I want Cursor on my laptop"
    result = graph.invoke(state)
    return result
