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

def head_to_head(player_a: str, player_b: str) -> dict:
    """Return the head-to-head win counts between two players.

    Counts matches each player won against the other, by exact name.
    """
    conn = get_connection()
    try:
        a_wins = conn.execute(
            "SELECT COUNT(*) FROM matches WHERE winner_name = ? AND loser_name = ?",
            (player_a, player_b),
        ).fetchone()[0]
        b_wins = conn.execute(
            "SELECT COUNT(*) FROM matches WHERE winner_name = ? AND loser_name = ?",
            (player_b, player_a),
        ).fetchone()[0]
        return {
            "player_a": player_a,
            "a_wins": a_wins,
            "player_b": player_b,
            "b_wins": b_wins,
            "total_meetings": a_wins + b_wins,
        }
    finally:
        conn.close()