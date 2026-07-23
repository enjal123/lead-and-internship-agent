import os
import tempfile

import utils.config as config
import database.db as db


def _use_temp_db():
    tmp_path = tempfile.mktemp(suffix=".db")
    config.DATABASE_PATH = tmp_path
    db.DATABASE_PATH = tmp_path
    db._initialized = False
    return tmp_path


def test_init_db_creates_tables():
    tmp_path = _use_temp_db()
    conn = db.connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cursor.fetchall()}
    conn.close()
    os.remove(tmp_path)

    assert {"businesses", "internships", "email_queue"}.issubset(tables)


def test_add_and_get_business():
    _use_temp_db()
    from database.business_queries import add_business, get_all_businesses

    add_business(
        business_name="Test Cafe",
        website="https://testcafe.example.com",
        email="hello@testcafe.example.com",
        phone=None,
        ai_analysis="Looks dated.",
        lead_score=7,
        outreach_email="Hi there...",
    )

    rows = get_all_businesses()
    assert len(rows) == 1
    assert rows[0]["business_name"] == "Test Cafe"
    assert rows[0]["lead_score"] == 7


def test_duplicate_website_is_ignored_not_crashed():
    _use_temp_db()
    from database.business_queries import add_business, get_all_businesses

    for _ in range(2):
        add_business(
            business_name="Test Cafe",
            website="https://testcafe.example.com",
            email="hello@testcafe.example.com",
            phone=None,
            ai_analysis="Looks dated.",
            lead_score=7,
            outreach_email="Hi there...",
        )

    rows = get_all_businesses()
    assert len(rows) == 1  # second insert silently ignored, not duplicated
