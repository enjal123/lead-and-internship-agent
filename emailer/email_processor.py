from database.queue_queries import get_pending_emails, mark_sent, mark_failed
from emailer.smtp_sender import send_email
from utils.logger import logger


def process_pending_emails():
    emails = get_pending_emails()

    for email in emails:
        try:
            send_email(email["recipient"], email["subject"], email["body"])
            mark_sent(email["id"])
        except Exception as e:
            logger.error(f"Failed to send email to {email['recipient']}: {e}")
            mark_failed(email["id"])
