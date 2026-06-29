"""Simple read queries against the matches table.

These are plain Python functions that run SQL and return results. Later, the
assistant will call functions like these as tools, but they are useful on their
own for exploring the data.
"""
from __future__ import annotations

from ace.db import get_connection


def player_win_count(name: str) -> int:
    """Return how many matches a player has won (by exact name)."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT COUNT(*) FROM matches WHERE winner_name = ?",
            (name,),
        ).fetchone()
        return row[0]
    finally:
        conn.close()


def total_matches() -> int:
    """Return the total number of matches in the database."""
    conn = get_connection()
    try:
        return conn.execute("SELECT COUNT(*) FROM matches").fetchone()[0]
    finally:
        conn.close()