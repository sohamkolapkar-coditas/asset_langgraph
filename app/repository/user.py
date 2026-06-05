from app.models.user import User
from sqlalchemy.orm import Session
from app.utils.constants.error_messages import ErrorMessages


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user(self, email: str):
        try:
            user = self.db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            raise Exception(ErrorMessages.DATABASE_ERROR.value)

    
