from database.db import connect_db


def add_business(business_name, website, email, phone, ai_analysis, lead_score, outreach_email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO businesses (
            business_name, website, email, phone,
            ai_analysis, lead_score, outreach_email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (business_name, website, email, phone, ai_analysis, lead_score, outreach_email),
    )

    conn.commit()
    conn.close()


def get_all_businesses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_uncontacted_businesses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses WHERE outreach_sent = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_contacted(business_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE businesses SET outreach_sent = 1 WHERE id = ?", (business_id,))
    conn.commit()
    conn.close()
