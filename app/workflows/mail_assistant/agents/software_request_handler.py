from langchain.agents import create_agent
from app.config.inference import llm_model
from app.workflows.mail_assistant.prompts.software_request_handler import (
    SOFTWARE_REQUEST_HANDLER_PROMPT,
)
from app.utils.tools.user_asset import user_asset
from app.utils.tools.asset_category_check import check_category
from app.utils.tools.check_user_asset_code import check_user_asset_code
from app.utils.tools.get_software import get_software


class SoftwareRequestHandlerAgent:

    software_request_handler_agent = create_agent(
        model=llm_model,
        system_prompt=SOFTWARE_REQUEST_HANDLER_PROMPT,
        tools=[user_asset, check_category,check_user_asset_code,get_software],
    )
