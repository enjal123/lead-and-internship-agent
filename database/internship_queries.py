from database.db import connect_db


def add_internship(company, title, job_description, link, freshman_friendly, ai_analysis, resume_text, outreach_email):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO internships (
            company, title, job_description, link,
            freshman_friendly, ai_analysis, resume_text, outreach_email
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (company, title, job_description, link, freshman_friendly, ai_analysis, resume_text, outreach_email),
    )

    conn.commit()
    conn.close()


def get_unapplied_internships():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM internships WHERE applied = 0")
    rows = cursor.fetchall()
    conn.close()
    return rows


def mark_applied(internship_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE internships SET applied = 1 WHERE id = ?", (internship_id,))
    conn.commit()
    conn.close()
