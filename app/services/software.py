from typing import Annotated
from fastapi import Depends
from app.repository.software import SoftwareRespository
from app.utils.init_repo import init_repo


class SoftwareService:

    def __init__(
        self,
        software_repo: Annotated[
            SoftwareRespository, init_repo(class_name=SoftwareRespository)
        ],
    ):
        self.software_repo = software_repo

    def get_software(self, name: str):
        try:
            software = self.software_repo.get_software(name)
            if not software:
                return False
            return software

        except Exception as e:
            raise e

    def get_softwares(self):
        try:
            softwares = self.software_repo.get_softwares()
            if not softwares:
                return False
            return softwares

        except Exception as e:
            raise e


def init_software_service():
    return SoftwareService(init_repo(class_name=SoftwareRespository))
