import re


def check_email(email: str) -> bool:
    """This tool is used to check if the email belongs to the coditas organization

    Args:
        email (str): Email of the sender
    """
    if bool(re.search(r"@coditas\.com$", email)):
        return True
    return False
