import pytest
import pandas as pd
from src.utils import load_csv, clean_phone, validate_email


# Tests for load_csv

def test_load_csv_file_not_found():
    """load_csv should raise FileNotFoundError for a missing file."""
    with pytest.raises(FileNotFoundError):
        load_csv("nonexistent_file.csv")


def test_load_csv_empty_file(tmp_path):
    """load_csv on an empty file should raise EmptyDataError."""
    empty = tmp_path / "empty.csv"
    empty.write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(str(empty))


def test_load_csv_success(tmp_path):
    """load_csv should return a DataFrame with the correct shape."""
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("customer_id,age\n1,25\n2,30\n")
    df = load_csv(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["customer_id", "age"]


# Tests for clean_phone

def test_clean_phone_dashes():
    """Dashes should be stripped, leaving only digits."""
    assert clean_phone("416-555-1234") == "4165551234"


def test_clean_phone_parentheses_and_spaces():
    """Parentheses and spaces should be stripped."""
    assert clean_phone("(416) 555 1234") == "4165551234"


def test_clean_phone_dots():
    """Dots should be stripped."""
    assert clean_phone("416.555.1234") == "4165551234"


def test_clean_phone_already_digits():
    """A string of digits should be returned unchanged."""
    assert clean_phone("4165551234") == "4165551234"


def test_clean_phone_invalid_none():
    """None input should return an empty string, not raise."""
    assert clean_phone(None) == ""


def test_clean_phone_empty_string():
    """Empty string should return an empty string."""
    assert clean_phone("") == ""


# Tests for validate_email

def test_validate_email_valid():
    """Standard email addresses should return True."""
    assert validate_email("user@example.com") is True


def test_validate_email_valid_subdomain():
    """Email with a subdomain should return True."""
    assert validate_email("user@mail.example.co.uk") is True


def test_validate_email_missing_at():
    """Email without an @ symbol should return False."""
    assert validate_email("userexample.com") is False


def test_validate_email_missing_domain():
    """Email with @ but no domain should return False."""
    assert validate_email("user@") is False


def test_validate_email_missing_local():
    """Email starting with @ should return False."""
    assert validate_email("@example.com") is False


def test_validate_email_none():
    """None input should return False, not raise."""
    assert validate_email(None) is False


def test_validate_email_empty_string():
    """Empty string should return False."""
    assert validate_email("") is False
    