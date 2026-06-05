from langchain.agents import create_agent
from app.config.inference import llm_model
from app.workflows.mail_assistant.prompts.issue_handler import ISSUE_HANDLER_PROMPT
from app.utils.tools.asset_category_check import check_category
from app.utils.tools.user_asset import user_asset
from app.utils.tools.check_user_asset_code import check_user_asset_code


class IssueHandlerAgent:

    issue_handler_agent = create_agent(
        model=llm_model,
        system_prompt=ISSUE_HANDLER_PROMPT,
        tools=[check_category, user_asset, check_user_asset_code],
    )
