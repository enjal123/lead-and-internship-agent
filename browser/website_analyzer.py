import requests
from bs4 import BeautifulSoup

from utils.config import REQUEST_TIMEOUT, USER_AGENT

HEADERS = {"User-Agent": USER_AGENT}


def analyze_website(url):
    analysis = {
        "has_ssl": False,
        "mobile_friendly": True,
        "has_meta_description": False,
        "has_h1": False,
        "outdated_ui": False,
        "performance_score": 5,
    }

    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)

        if url.startswith("https"):
            analysis["has_ssl"] = True

        soup = BeautifulSoup(response.text, "html.parser")

        if soup.find("meta", attrs={"name": "description"}):
            analysis["has_meta_description"] = True

        if soup.find("h1"):
            analysis["has_h1"] = True

        text = soup.get_text().lower()

        if "best viewed on desktop" in text:
            analysis["mobile_friendly"] = False

        if len(text) < 500:
            analysis["outdated_ui"] = True

    except Exception:
        analysis["performance_score"] = 1

    return analysis
