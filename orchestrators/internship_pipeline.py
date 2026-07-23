"""
End-to-end internship discovery pipeline:

  1. search for internship postings (free search, see browser/internship_scraper.py)
  2. have the LLM assess fit for the candidate background (utils/config.py)
  3. tailor the resume for postings worth applying to
  4. save everything to the database

Run with: python main.py internships
"""
from tqdm import tqdm

from browser.internship_scraper import scrape_internships
from browser.scraper import extract_text, get_html
from agents.internship_agent import analyze_job
from ai.classifiers import is_freshman_friendly
from resume.templates.resume_builder import build_resume_for_job
from database.internship_queries import add_internship
from utils.helpers import truncate
from utils.rate_limiter import polite_delay
from utils.logger import logger


BLACKLISTED_URL_PARTS = (
    "youtube.com",
    "youtu.be",
    "medium.com",
    "reddit.com",
    "coursera.org",
    "udemy.com",
    "github.com/pittcsc",
    "github.com/SimplifyJobs",
)
BLACKLISTED_TITLE_TERMS = (
    "how to",
    "crash course",
    "guide",
    "roadmap",
    "tips",
    "questions",
    "interview prep",
    "top 10",
    "list of",
)
ATS_SIGNATURES = (
    "boards.greenhouse.io",
    "jobs.lever.co",
    "jobs.ashbyhq.com",
    "myworkdayjobs.com",
    "/jobs/",
    "/careers/",
    "/position/",
)


def is_likely_job_posting(url: str, title: str) -> bool:
    """Return True for likely job postings while filtering obvious non-job content."""
    normalized_url = (url or "").lower()
    normalized_title = (title or "").lower()

    if not normalized_url and not normalized_title:
        return False

    for blocked_part in BLACKLISTED_URL_PARTS:
        if blocked_part.lower() in normalized_url:
            return False

    for blocked_term in BLACKLISTED_TITLE_TERMS:
        if blocked_term.lower() in normalized_title:
            return False

    if any(signature in normalized_url for signature in ATS_SIGNATURES):
        return True

    return True


def run_internship_pipeline(query: str = None, max_results: int = 10, build_resumes: bool = True):
    logger.info("Starting internship discovery pipeline...")
    postings = scrape_internships(search_query=query, max_results=max_results, fetch_descriptions=False)

    if not postings:
        logger.info("No internship postings found for this query.")
        return []

    saved = []

    for posting in tqdm(postings, desc="Analyzing internships"):
        company = posting["company"]
        title = posting["title"]
        link = posting["link"]

        if not is_likely_job_posting(link, title):
            logger.info(f"Ignoring non-job posting: {title} ({link})")
            polite_delay()
            continue

        description = posting.get("description") or ""
        if not description:
            try:
                html = get_html(link)
                description = truncate(extract_text(html), 2000)
            except Exception as e:
                logger.error(f"Could not fetch internship page {link}: {e}")
                description = title

        description = (description or title)[:2000]

        try:
            ai_analysis = analyze_job(description)
            good_fit = is_freshman_friendly(description)

            resume_path = None
            if build_resumes and good_fit:
                try:
                    resume_path = build_resume_for_job(company, description)
                except FileNotFoundError as e:
                    logger.error(str(e))

            add_internship(
                company=company,
                title=title,
                job_description=description,
                link=link,
                freshman_friendly=1 if good_fit else 0,
                ai_analysis=ai_analysis,
                resume_text=resume_path or "",
                outreach_email="",
            )

            saved.append({"title": title, "link": link, "good_fit": good_fit})
            logger.info(f"Saved internship: {title} — good fit: {good_fit}")

        except Exception as e:
            logger.error(f"Failed to process internship '{title}' ({link}): {e}")

        polite_delay()

    logger.info(f"Internship pipeline complete. Saved {len(saved)} posting(s).")
    return saved
