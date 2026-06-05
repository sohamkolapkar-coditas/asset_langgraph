from app.services.user import init_user_service

user_service = init_user_service()


def check_user(email: str):
    """This tool is used to check if the user exists in the database

    Args:
        email (str): Email of the sender
    """
    user = user_service.get_user(email)
    if user:
        return {
            "id": str(user.id),
            "email": user.email,
        }
    return False
