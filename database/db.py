"""
SQLite connection helper.

NOTE: nothing in the original project ever executed schema.sql, so the
businesses/internships/email_queue tables were never created and every
query against them would fail with "no such table". `init_db()` fixes
that and is called automatically the first time a connection is opened.
"""
import os
import sqlite3

from utils.config import DATABASE_PATH

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

_initialized = False


def init_db():
    global _initialized
    conn = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    _initialized = True


def connect_db():
    if not _initialized:
        init_db()
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn
