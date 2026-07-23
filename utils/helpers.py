"""Miscellaneous small helper functions shared across the codebase."""


def truncate(text, max_length=4000):
    if not text:
        return ""
    return text[:max_length]


def safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clean_whitespace(text):
    if not text:
        return ""
    return " ".join(text.split())


def slugify(text):
    """Turns arbitrary text into a filesystem-safe slug, e.g. for filenames."""
    raw = "".join(c if c.isalnum() else "_" for c in text)
    collapsed = "_".join(part for part in raw.split("_") if part)
    return collapsed or "untitled"
