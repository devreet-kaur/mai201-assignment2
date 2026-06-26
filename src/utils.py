import pandas as pd
import re


def load_csv(filepath: str) -> pd.DataFrame:
    """Load a CSV file and return a DataFrame."""
    return pd.read_csv(filepath)


def clean_phone(phone: str) -> str:
    """
    Normalize a phone number to digits only.
    Returns only the digit characters from the input.
    Returns an empty string if the input is None or not a string.
    """
    if not isinstance(phone, str):
        return ""
    return re.sub(r"\D", "", phone)


def validate_email(email: str) -> bool:
    """
    Return True if the email matches a basic valid format, False otherwise.
    """
    if not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))
