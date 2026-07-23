"""Lightweight validation helpers (no external dependency required)."""
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
URL_REGEX = re.compile(r"^https?://[^\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(email and EMAIL_REGEX.match(email.strip()))


def is_valid_url(url: str) -> bool:
    return bool(url and URL_REGEX.match(url.strip()))


def clean_website_url(url: str) -> str:
    """Normalizes a website URL so lookups/dedup keys match consistently."""
    if not url:
        return ""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")
