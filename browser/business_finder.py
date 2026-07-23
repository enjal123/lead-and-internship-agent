"""
Finds candidate local business websites to evaluate as leads.

Default path: free DuckDuckGo search, no API key, no cost.

Optional path: if you set GOOGLE_PLACES_API_KEY in .env, `find_businesses`
will use the Google Places Text Search API instead, which returns
cleaner business names/addresses but is a paid API past its free
monthly quota. It is entirely opt-in -- leave the key unset and this
module never touches it or costs anything.
"""
import requests

from browser.scraper import duckduckgo_search
from utils.config import BUSINESS_SEARCH_QUERY, GOOGLE_PLACES_API_KEY, REQUEST_TIMEOUT
from utils.logger import logger


def _find_businesses_free(query, max_results):
    """No-cost path: DuckDuckGo search results treated as candidate leads."""
    results = duckduckgo_search(query, max_results=max_results)
    return [
        {"business_name": r["title"], "website": r["link"]}
        for r in results
    ]


def _find_businesses_google_places(query, max_results):
    """
    Optional, paid path (only used if GOOGLE_PLACES_API_KEY is set).
    https://developers.google.com/maps/documentation/places/web-service/text-search
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": GOOGLE_PLACES_API_KEY}

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    data = response.json()

    leads = []
    for place in data.get("results", [])[:max_results]:
        leads.append({
            "business_name": place.get("name", "Unknown"),
            "website": place.get("formatted_address", ""),  # Places Text Search
            "place_id": place.get("place_id"),               # doesn't return a
        })                                                    # website URL directly;
    return leads                                              # see README for the
                                                               # Place Details follow-up call.


def find_businesses(query: str = None, max_results: int = 10):
    query = query or BUSINESS_SEARCH_QUERY

    if GOOGLE_PLACES_API_KEY:
        logger.info(f"Searching businesses via Google Places: '{query}'")
        try:
            return _find_businesses_google_places(query, max_results)
        except Exception as e:
            logger.error(f"Google Places search failed, falling back to free search: {e}")

    logger.info(f"Searching businesses via free search: '{query}'")
    return _find_businesses_free(query, max_results)
