from sqlalchemy.orm import Session
from app.models.session import db


def init_repo(class_name=None, db: Session = db):
    return class_name(db)
