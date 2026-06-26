"""SQLite database access for Ace.

A thin wrapper around the standard library's sqlite3. The database is a single
file on disk (its location comes from config). Use ``get_connection`` to open it;
rows come back as ``sqlite3.Row`` so you can read columns by name.
"""
from __future__ import annotations

import sqlite3

from ace.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Open the Ace database and return a connection.

    Creates the database file (and its parent folder) on first use. Column
    access by name is enabled via the row factory.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn