"""
Long-running worker that processes the email queue every 10 minutes.
Run with: python -m emailer.queue_manager
"""
import time

from emailer.email_processor import process_pending_emails
from utils.logger import logger

CHECK_INTERVAL_SECONDS = 600


def run_email_queue():
    logger.info("Email queue worker started.")
    while True:
        process_pending_emails()
        time.sleep(CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_email_queue()
