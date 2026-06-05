from langchain.tools import tool
from app.services.software import init_software_service

software_service = init_software_service()


@tool
def get_software(name: str):
    """This tool allows the agent to retrieve the software by its name and check if it exists in the system.

    Args:
        name(str): name of the software
    """
    software = software_service.get_software(name)
    if not software:
        return "Software not found in the database."
    return {"id": str(software.id), "name": software.name}
