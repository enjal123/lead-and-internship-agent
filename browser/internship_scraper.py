"""
Finds candidate internship postings.

The original implementation drove a headless Chromium browser against
Google search results and only ever kept a raw <h3> title -- no
company, no link, no description -- and Google routinely blocks/
CAPTCHAs this kind of automated traffic anyway, which is the main
reason it never surfaced usable results.

This version searches via DuckDuckGo's HTML endpoint (free, no API key,
no headless browser needed) and then fetches each result page to pull
real text for the AI analysis agents to work with.
"""
from browser.scraper import duckduckgo_search, get_html, extract_text
from utils.config import INTERNSHIP_SEARCH_QUERY
from utils.rate_limiter import polite_delay
from utils.helpers import truncate
from utils.logger import logger


def scrape_internships(search_query: str = None, max_results: int = 10, fetch_descriptions: bool = True):
    """
    Returns a list of dicts: {"company", "title", "description", "link"}.
    `company` is left as "Unknown" -- the AI analysis agents (see
    agents/internship_agent.py) work fine on the title + description
    alone, and reliably parsing a company name out of arbitrary result
    titles is fragile; feel free to refine this per job board if you
    target a specific one.
    """
    query = search_query or INTERNSHIP_SEARCH_QUERY
    logger.info(f"Searching internships: '{query}'")

    raw_results = duckduckgo_search(query, max_results=max_results)
    internships = []

    for item in raw_results:
        description = ""
        if fetch_descriptions:
            try:
                html = get_html(item["link"])
                description = truncate(extract_text(html), 2000)
            except Exception as e:
                logger.error(f"Could not fetch internship page {item['link']}: {e}")
            polite_delay()

        internships.append({
            "company": "Unknown",
            "title": item["title"],
            "description": description,
            "link": item["link"],
        })

    logger.info(f"Found {len(internships)} internship postings")
    return internships
