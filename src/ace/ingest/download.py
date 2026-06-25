"""Download raw ATP match data into ``data/raw``.

Source: the Tennismylife TML-Database (https://github.com/Tennismylife/TML-Database),
a maintained ATP results dataset in the column format popularised by Jeff
Sackmann, sourced from the official ATP site. Used for educational and
analytical purposes with attribution.

One file per season (e.g. ``2024.csv``) plus a player table (``ATP_Database.csv``).
Re-running skips files already present, so it is safe to run repeatedly. Widen
``YEARS`` toward 1968 for a deeper history.

Run with:

    python -m ace.ingest.download
"""
from __future__ import annotations

import sys

import requests

from ace.config import RAW_DATA_DIR

TML_BASE = "https://raw.githubusercontent.com/Tennismylife/TML-Database/master"

# One CSV per season. Widen this range for more history (data goes back to 1968).
YEARS = range(2004, 2026)

FILES = [f"{TML_BASE}/ATP_Database.csv"] + [f"{TML_BASE}/{year}.csv" for year in YEARS]


def download(url: str) -> None:
    """Fetch a single file into data/raw, skipping it if already downloaded."""
    name = url.rsplit("/", 1)[-1]
    dest = RAW_DATA_DIR / name
    if dest.exists():
        print(f"skip   {name} (already downloaded)")
        return

    print(f"fetch  {name} ...")
    resp = requests.get(url, timeout=60)
    if resp.status_code == 404:
        print(f"miss   {name} (not found, skipping)")
        return
    resp.raise_for_status()

    dest.write_bytes(resp.content)
    print(f"done   {name} ({len(resp.content):,} bytes)")


def main() -> int:
    """Download every file in FILES into data/raw."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    for url in FILES:
        download(url)
    print(f"\nRaw data is in {RAW_DATA_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
