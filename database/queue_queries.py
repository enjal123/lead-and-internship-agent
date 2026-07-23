from database.db import connect_db


def add_email_to_queue(recipient, subject, body):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO email_queue (recipient, subject, body)
        VALUES (?, ?, ?)
        """,
        (recipient, subject, body),
    )

    conn.commit()
    conn.close()


def get_pending_emails():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM email_queue
        WHERE status = 'pending'
        ORDER BY created_at ASC
        """
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_sent(email_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE email_queue SET status = 'sent', sent_at = CURRENT_TIMESTAMP WHERE id = ?",
        (email_id,),
    )
    conn.commit()
    conn.close()


def mark_failed(email_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE email_queue SET status = 'failed' WHERE id = ?", (email_id,))
    conn.commit()
    conn.close()
