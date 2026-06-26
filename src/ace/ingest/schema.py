"""Database schema for Ace.

Defines the tables. Right now that's the ``matches`` table, whose columns mirror
the ATP match CSVs. Call ``create_tables`` to set up an empty database; it is
safe to run repeatedly (it only creates tables that do not already exist).
"""
from __future__ import annotations

from ace.db import get_connection

CREATE_MATCHES = """
CREATE TABLE IF NOT EXISTS matches (
    tourney_id        TEXT,
    tourney_name      TEXT,
    surface           TEXT,
    draw_size         INTEGER,
    tourney_level     TEXT,
    tourney_date      INTEGER,
    match_num         INTEGER,

    winner_id         INTEGER,
    winner_seed       TEXT,
    winner_entry      TEXT,
    winner_name       TEXT,
    winner_hand       TEXT,
    winner_ht         INTEGER,
    winner_ioc        TEXT,
    winner_age        REAL,
    winner_rank       INTEGER,
    winner_rank_points INTEGER,

    loser_id          INTEGER,
    loser_seed        TEXT,
    loser_entry       TEXT,
    loser_name        TEXT,
    loser_hand        TEXT,
    loser_ht          INTEGER,
    loser_ioc         TEXT,
    loser_age         REAL,
    loser_rank        INTEGER,
    loser_rank_points INTEGER,

    score             TEXT,
    best_of           INTEGER,
    round             TEXT,
    minutes           INTEGER,

    w_ace             INTEGER,
    w_df              INTEGER,
    w_svpt            INTEGER,
    w_1stIn           INTEGER,
    w_1stWon          INTEGER,
    w_2ndWon          INTEGER,
    w_SvGms           INTEGER,
    w_bpSaved         INTEGER,
    w_bpFaced         INTEGER,

    l_ace             INTEGER,
    l_df              INTEGER,
    l_svpt            INTEGER,
    l_1stIn           INTEGER,
    l_1stWon          INTEGER,
    l_2ndWon          INTEGER,
    l_SvGms           INTEGER,
    l_bpSaved         INTEGER,
    l_bpFaced         INTEGER
)
"""

def create_tables() -> None:
    """Create all tables if they do not already exist."""
    conn = get_connection()
    try:
        conn.execute(CREATE_MATCHES)
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tables created (or already present).")