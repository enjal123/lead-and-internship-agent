"""
End-to-end business lead pipeline:

  1. find candidate business websites (free search, see browser/business_finder.py)
  2. analyze each site's quality (browser/website_analyzer.py)
  3. have the LLM assess it as a lead + generate an outreach email
  4. score the lead and save everything to the database

Run with: python main.py businesses
"""
from tqdm import tqdm

from browser.business_finder import find_businesses
from browser.business_scraper import extract_emails_from_website
from browser.website_analyzer import analyze_website
from agents.client_agent import analyze_business
from agents.outreach_agent import generate_outreach
from agents.scoring_agent import score_lead
from database.business_queries import add_business
from utils.rate_limiter import polite_delay
from utils.validators import clean_website_url
from utils.logger import logger


def run_business_pipeline(query: str = None, max_results: int = 10):
    logger.info("Starting business lead pipeline...")
    leads = find_businesses(query=query, max_results=max_results)

    if not leads:
        logger.info("No candidate businesses found for this query.")
        return []

    saved = []

    for lead in tqdm(leads, desc="Analyzing business leads"):
        website = clean_website_url(lead.get("website", ""))
        business_name = lead.get("business_name", "Unknown")

        if not website:
            continue

        try:
            site_quality = analyze_website(website)
            website_issues = ", ".join(
                k for k, v in site_quality.items() if v in (False, True) and
                ((k in ("outdated_ui",) and v) or (k in ("has_ssl", "has_meta_description", "has_h1") and not v))
            ) or "None obviously detected"

            ai_analysis = analyze_business(business_name, website)
            lead_score = score_lead(ai_analysis)
            outreach_email = generate_outreach(
                business_name=business_name,
                website=website,
                website_issues=website_issues,
            )

            emails = extract_emails_from_website(website)
            contact_email = emails[0] if emails else None

            add_business(
                business_name=business_name,
                website=website,
                email=contact_email,
                phone=None,
                ai_analysis=ai_analysis,
                lead_score=lead_score,
                outreach_email=outreach_email,
            )

            saved.append({"business_name": business_name, "website": website, "lead_score": lead_score})
            logger.info(f"Saved lead: {business_name} ({website}) — score {lead_score}/10")

        except Exception as e:
            logger.error(f"Failed to process business {business_name} ({website}): {e}")

        polite_delay()

    logger.info(f"Business pipeline complete. Saved {len(saved)} lead(s).")
    return saved
