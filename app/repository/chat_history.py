from app.models.chat_history import ChatHistory
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.utils.constants.error_messages import ErrorMessages


class ChatHistoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def add_user_prompt(self, user_prompt: str, thread_id: str):
        try:
            self.db.add(
                ChatHistory(role="user", message=user_prompt, thread_id=thread_id)
            )
            self.db.commit()
            return True
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def add_llm_response(self, llm_response: str, thread_id: str):
        try:
            self.db.add(
                ChatHistory(
                    role="assitant",
                    message=llm_response,
                    thread_id=thread_id,
                )
            )
            self.db.commit()
            return True
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def add_tool_response(self, tool_message: str, thread_id: str):
        try:
            self.db.add(
                ChatHistory(
                    role="tool",
                    message=tool_message,
                    thread_id=thread_id,
                )
            )
            self.db.commit()
            return True
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    def get_chat_history(self, thread_id: str):
        try:
            response_list = []
            history = (
                self.db.query(ChatHistory)
                .filter(ChatHistory.thread_id == thread_id)
                .order_by(desc(ChatHistory.created_at))
                .limit(20)
                .all()
            )
            for chat in history:
                response_dict = {}
                response_dict["role"] = chat.role
                response_dict["message"] = chat.message
                response_list.append(response_dict)
            return response_list
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)
