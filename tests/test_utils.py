from utils.validators import is_valid_email, is_valid_url, clean_website_url
from utils.helpers import truncate, safe_int, clean_whitespace, slugify


def test_is_valid_email():
    assert is_valid_email("someone@example.com")
    assert not is_valid_email("not-an-email")
    assert not is_valid_email("")


def test_is_valid_url():
    assert is_valid_url("https://example.com")
    assert not is_valid_url("example.com")


def test_clean_website_url():
    assert clean_website_url("example.com") == "https://example.com"
    assert clean_website_url("https://example.com/") == "https://example.com"


def test_truncate():
    assert truncate("hello world", 5) == "hello"
    assert truncate("", 5) == ""


def test_safe_int():
    assert safe_int("42") == 42
    assert safe_int("not a number", default=-1) == -1


def test_clean_whitespace():
    assert clean_whitespace("  hello   world  ") == "hello world"


def test_slugify():
    assert slugify("Joe's Pizza & Grill!") == "Joe_s_Pizza_Grill"
