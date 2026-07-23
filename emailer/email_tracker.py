"""
Very lightweight send tracking on top of the email_queue table -- how
many emails have been sent vs failed vs are still pending.
"""
from database.db import connect_db


def get_email_stats():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT status, COUNT(*) as count FROM email_queue GROUP BY status")
    rows = cursor.fetchall()
    conn.close()
    return {row["status"]: row["count"] for row in rows}
