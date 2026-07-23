from browser.scraper import get_html, extract_text


def detect_business_qualify(url):
    """
    Cheap heuristic pre-filter (no LLM call) to flag websites that are
    likely outdated before spending an AI call analyzing them.
    """
    try:
        html = get_html(url)
        text = extract_text(html).lower()

        score = 0
        if "wordpress" in text:
            score += 1
        if "copyright" in text:
            score += 1
        if len(text) < 500:
            score += 2

        return {"outdated": score >= 2, "score": score}

    except Exception:
        return {"outdated": False, "score": 0}
