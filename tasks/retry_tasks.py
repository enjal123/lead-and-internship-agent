"""
Requeues failed emails as pending so the queue worker retries them.
Run with: python -m tasks.retry_tasks
"""
from database.db import connect_db
from utils.logger import logger


def retry_failed_emails():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE email_queue SET status = 'pending' WHERE status = 'failed'")
    retried = cursor.rowcount
    conn.commit()
    conn.close()
    logger.info(f"Requeued {retried} failed email(s) for retry.")
    return retried


if __name__ == "__main__":
    retry_failed_emails()
