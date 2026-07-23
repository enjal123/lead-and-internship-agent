"""
Housekeeping tasks: clears out old failed email_queue rows and old
generated resumes so the project doesn't accumulate cruft over time.

Run with: python -m tasks.cleanup_tasks
"""
import os
import time

from database.db import connect_db
from utils.logger import logger

GENERATED_RESUME_DIR = "resume/generated"
MAX_RESUME_AGE_DAYS = 30


def clear_failed_emails():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM email_queue WHERE status = 'failed'")
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    logger.info(f"Cleared {deleted} failed email(s) from the queue.")
    return deleted


def clear_old_generated_resumes(max_age_days: int = MAX_RESUME_AGE_DAYS):
    if not os.path.isdir(GENERATED_RESUME_DIR):
        return 0

    cutoff = time.time() - (max_age_days * 86400)
    removed = 0

    for filename in os.listdir(GENERATED_RESUME_DIR):
        if filename == ".gitkeep":
            continue
        path = os.path.join(GENERATED_RESUME_DIR, filename)
        if os.path.isfile(path) and os.path.getmtime(path) < cutoff:
            os.remove(path)
            removed += 1

    logger.info(f"Removed {removed} generated resume(s) older than {max_age_days} days.")
    return removed


if __name__ == "__main__":
    clear_failed_emails()
    clear_old_generated_resumes()
