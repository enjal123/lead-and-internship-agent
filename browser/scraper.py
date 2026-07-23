"""
Core HTTP scraping helpers.

Search uses free, no-API-key sources (DuckDuckGo Lite, DuckDuckGo's
static HTML endpoint, then Bing HTML as a fallback) rather than scraping
Google directly, which requires a headless browser and reliably
triggers a CAPTCHA wall.
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote
from ddgs import DDGS

from utils.config import USER_AGENT, REQUEST_TIMEOUT
from utils.logger import logger

HEADERS = {"User-Agent": USER_AGENT}


def get_html(url):
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def get_soup(html):
    return BeautifulSoup(html, "html.parser")


def extract_text(html):
    # NOTE: BeautifulSoup's `.text` is a property, not a callable --
    # `soup.text(...)` raises "'str' object is not callable". Use
    # `get_text(separator=...)` instead.
    soup = get_soup(html)
    return soup.get_text(separator=" ", strip=True)


def extract_links(html):
    soup = get_soup(html)
    return [tag["href"] for tag in soup.find_all("a", href=True)]


def _resolve_ddg_link(href):
    """
    DuckDuckGo sometimes wraps result links in a redirect like
    "//duckduckgo.com/l/?uddg=<url-encoded-target>&rut=...". Unwrap it so
    we store/fetch the real destination URL instead of a DDG redirect.
    """
    if not href:
        return href
    if href.startswith("//"):
        href = "https:" + href
    if "duckduckgo.com/l/" in href:
        parsed = urlparse(href)
        target = parse_qs(parsed.query).get("uddg")
        if target:
            return unquote(target[0])
    return href


def _parse_ddg_lite(html):
    soup = get_soup(html)
    results = []
    for tag in soup.select("a.result-link"):
        title = tag.get_text(strip=True)
        link = _resolve_ddg_link(tag.get("href"))
        if title and link:
            results.append({"title": title, "link": link})
    return results


def _parse_ddg_html(html):
    soup = get_soup(html)
    results = []
    for tag in soup.select("a.result__a"):
        title = tag.get_text(strip=True)
        link = _resolve_ddg_link(tag.get("href"))
        if title and link:
            results.append({"title": title, "link": link})
    return results


def _parse_bing(html):
    soup = get_soup(html)
    results = []
    for item in soup.select("li.b_algo"):
        link_tag = item.select_one("h2 a")
        if link_tag and link_tag.get("href"):
            results.append({
                "title": link_tag.get_text(strip=True),
                "link": link_tag["href"],
            })
    return results


def _search_source(name, method, url, parser, max_results, **request_kwargs):
    try:
        response = method(url, timeout=REQUEST_TIMEOUT, **request_kwargs)
        response.raise_for_status()
        results = parser(response.text)[:max_results]
        logger.info(
            f"[{name}] response {response.status_code}, "
            f"{len(response.text)} bytes, {len(results)} result(s) parsed"
        )
        return results
    except Exception as e:
        logger.error(f"[{name}] search failed: {e}")
        return []


def duckduckgo_search(query, max_results=10):
    """
    Free, no-API-key web search. Tries multiple sources in order, since
    any single one of these can start soft-blocking automated traffic
    (returning a normal-looking 200 OK page with zero matching results,
    rather than an error) without warning. Each attempt is logged so a
    "0 results" run can be diagnosed from logs.diagnostics after the fact.
    """
    # 1. Primary: use the official `ddgs` client (DDGS) and try specific backends
    results = []
    for backend in ("html", "lite"):
        try:
            with DDGS() as ddgs:
                for r in ddgs.text(query, backend=backend, max_results=max_results):
                    title = r.get("title") or r.get("text") or ""
                    link = r.get("href") or r.get("url") or r.get("link")
                    snippet = r.get("body") or r.get("snippet") or ""
                    if title and link:
                        results.append({
                            "title": title,
                            "link": link,
                            "url": link,
                            "snippet": snippet,
                            "body": snippet,
                        })
            if results:
                logger.info(f"[duckduckgo-ddgs:{backend}] {len(results)} result(s) parsed")
                return results
        except Exception as e:
            logger.warning(f"DDGS backend '{backend}' failed for query '{query}': {e}")
            continue

    # 2. Fallback: Bing HTML as a last resort (preserve previous behavior)
    browser_headers = {
        **HEADERS,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://duckduckgo.com/",
    }

    results = _search_source(
        "bing", requests.get,
        "https://www.bing.com/search",
        _parse_bing, max_results,
        params={"q": query}, headers=browser_headers,
    )
    if results:
        # Ensure each result has a `snippet` field for compatibility
        for r in results:
            if "snippet" not in r:
                r["snippet"] = ""
        return results

    logger.error(
        f"All search sources returned zero results for '{query}'. "
        "This usually means the search provider is soft-blocking "
        "automated requests rather than the query having no matches -- "
        "try again in a few minutes, from a different network, or with "
        "a broader query to confirm."
    )
    return []
