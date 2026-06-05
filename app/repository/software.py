from app.models.software import Software
from sqlalchemy.orm import Session
from app.utils.constants.error_messages import ErrorMessages
from sqlalchemy import and_


class SoftwareRespository:

    def __init__(self, db: Session):
        self.db = db

    def get_software(self, name: str):
        software = (
            self.db.query(Software)
            .filter(and_(Software.name == name.lower(), Software.is_active))
            .first()
        )
        return software

    def get_softwares(self):
        softwares = self.db.query(Software).filter(Software.is_active).all()
        return softwares
