"""Load the downloaded ATP match CSVs into the SQLite ``matches`` table.

Reads every season file in data/raw, keeps only the columns defined in the
schema, and writes the rows into the database. Re-running clears the table
first, so the result is always a clean, duplicate-free load.

Run with:

    python -m ace.ingest.load
"""
from __future__ import annotations

import sys

import pandas as pd

from ace.config import RAW_DATA_DIR
from ace.db import get_connection
from ace.ingest.schema import create_tables

# The match CSVs are the per-season files. The player file is named differently,
# so this pattern naturally excludes it.
SEASON_GLOB = "[0-9][0-9][0-9][0-9].csv"

# Columns the matches table knows about (must match schema.py).
MATCH_COLUMNS = [
    "tourney_id", "tourney_name", "surface", "draw_size", "tourney_level",
    "tourney_date", "match_num",
    "winner_id", "winner_seed", "winner_entry", "winner_name", "winner_hand",
    "winner_ht", "winner_ioc", "winner_age", "winner_rank", "winner_rank_points",
    "loser_id", "loser_seed", "loser_entry", "loser_name", "loser_hand",
    "loser_ht", "loser_ioc", "loser_age", "loser_rank", "loser_rank_points",
    "score", "best_of", "round", "minutes",
    "w_ace", "w_df", "w_svpt", "w_1stIn", "w_1stWon", "w_2ndWon", "w_SvGms",
    "w_bpSaved", "w_bpFaced",
    "l_ace", "l_df", "l_svpt", "l_1stIn", "l_1stWon", "l_2ndWon", "l_SvGms",
    "l_bpSaved", "l_bpFaced",
]


def load_matches() -> int:
    """Load all season CSVs into the matches table. Returns the row count."""
    create_tables()

    season_files = sorted(RAW_DATA_DIR.glob(SEASON_GLOB))
    if not season_files:
        print(f"No season files found in {RAW_DATA_DIR}. Run the downloader first.")
        return 0

    conn = get_connection()
    try:
        # Start clean so re-running never duplicates rows.
        conn.execute("DELETE FROM matches")
        conn.commit()

        total = 0
        for path in season_files:
            frame = pd.read_csv(path)
            # Keep only known columns, in the schema's order.
            frame = frame[[c for c in MATCH_COLUMNS if c in frame.columns]]
            frame.to_sql("matches", conn, if_exists="append", index=False)
            total += len(frame)
            print(f"loaded {len(frame):>4} matches from {path.name}")

        conn.commit()
        print(f"\nTotal matches loaded: {total}")
        return total
    finally:
        conn.close()


def main() -> int:
    load_matches()
    return 0


if __name__ == "__main__":
    sys.exit(main())