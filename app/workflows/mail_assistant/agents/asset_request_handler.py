from langchain.agents import create_agent
from app.config.inference import llm_model
from app.workflows.mail_assistant.prompts.asset_request_handler import (
    ASSET_REQUEST_HANDLER_PROMPT,
)
from app.utils.tools.asset_category_check import check_category
from app.utils.tools.get_asset import get_asset


class AssetRequestHandlerAgent:

    asset_request_handler_agent = create_agent(
        model=llm_model,
        system_prompt=ASSET_REQUEST_HANDLER_PROMPT, 
        tools=[check_category, get_asset],
    )
