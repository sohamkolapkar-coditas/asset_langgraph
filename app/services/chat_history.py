from typing import Annotated
from fastapi import Depends
from app.repository.chat_history import ChatHistoryRepository
from app.utils.init_repo import init_repo
from app.utils.constants.response_messages import ResponseMessages


class ChatHistoryService:

    def __init__(
        self,
        chat_history_repo: Annotated[
            ChatHistoryRepository, Depends(init_repo(class_name=ChatHistoryRepository))
        ],
    ):
        self.chat_history_repo = chat_history_repo

    def add_user_prompt(self, user_prompt: str, thread_id: str):
        try:
            if self.chat_history_repo.add_user_prompt(user_prompt, thread_id):
                return ResponseMessages.USER_PROMPT_ADDED_SUCCESSFULLY.value

        except Exception as e:
            raise e

    def add_llm_response(self, llm_response: str, thread_id: str):
        try:
            if self.chat_history_repo.add_llm_response(llm_response, thread_id):
                return ResponseMessages.LLM_RESPONSE_ADDED_SUCCESSFULLY.value

        except Exception as e:
            raise e

    def add_tool_response(self, tool_message: str, thread_id: str):
        try:
            if self.chat_history_repo.add_tool_response(tool_message, thread_id):
                return ResponseMessages.TOOL_RESPONSE_ADDED_SUCCESSFULLY.value

        except Exception as e:
            raise e

    def get_chat_history(self, thread_id: str):
        try:
            chat_history = self.chat_history_repo.get_chat_history(thread_id)
            return chat_history

        except Exception as e:
            raise e


def init_chat_history_service():
    return ChatHistoryService(init_repo(class_name=ChatHistoryRepository))
