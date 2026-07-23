"""
Finds contact info on a business's own website.

(The original project had this exact logic duplicated in two files --
business_scraper.py and email_extracter.py. Consolidated into one.)
"""
import re
import requests

from utils.config import REQUEST_TIMEOUT, USER_AGENT

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
HEADERS = {"User-Agent": USER_AGENT}

COMMON_CONTACT_PATHS = ["/contact", "/contact-us", "/about", "/support"]


def extract_emails_from_text(text):
    return list(set(re.findall(EMAIL_REGEX, text)))


def extract_emails_from_website(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        return extract_emails_from_text(response.text)
    except Exception:
        return []


def find_contact_page(base_url):
    for path in COMMON_CONTACT_PATHS:
        url = base_url.rstrip("/") + path
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
            if response.status_code == 200:
                return url
        except Exception:
            continue
    return None
