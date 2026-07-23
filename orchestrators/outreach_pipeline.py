"""
Queues outreach emails for any saved business leads that haven't been
contacted yet, then drains the queue (sends them).

Run with: python main.py outreach
"""
from database.business_queries import get_uncontacted_businesses, mark_contacted
from database.queue_queries import add_email_to_queue
from emailer.email_processor import process_pending_emails
from utils.validators import is_valid_email
from utils.logger import logger


def run_outreach_pipeline(send: bool = False):
    logger.info("Starting outreach pipeline...")
    leads = get_uncontacted_businesses()

    if not leads:
        logger.info("No uncontacted leads to reach out to.")
        return 0

    queued = 0

    for lead in leads:
        if not lead["email"] or not is_valid_email(lead["email"]):
            logger.info(f"Skipping {lead['business_name']} — no valid contact email found.")
            continue

        if not lead["outreach_email"]:
            logger.info(f"Skipping {lead['business_name']} — no outreach email generated yet.")
            continue

        add_email_to_queue(
            recipient=lead["email"],
            subject=f"quick thought about {lead['business_name']}'s website",
            body=lead["outreach_email"],
        )
        mark_contacted(lead["id"])
        queued += 1

    logger.info(f"Queued {queued} outreach email(s).")

    if send and queued:
        logger.info("Sending queued emails now...")
        process_pending_emails()

    return queued
