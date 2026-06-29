"""Central configuration for Ace.

Loads environment variables and defines the paths and model defaults used
across the project. Import ``settings`` from here rather than reading
``os.environ`` in several different places.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load variables from a local .env file if one exists.
load_dotenv()

# This file lives at src/ace/config.py, so the project root is two levels up.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
TEXT_DATA_DIR = DATA_DIR / "text"
DB_PATH = DATA_DIR / "ace.db"
CHROMA_DIR = DATA_DIR / "chroma"


@dataclass(frozen=True)
class Settings:
    """Runtime settings, assembled once at import time."""

    gemini_api_key: str | None
    chat_model: str
    db_path: Path
    chroma_dir: Path
    raw_data_dir: Path
    text_data_dir: Path


settings = Settings(
    gemini_api_key=os.getenv("GEMINI_API_KEY"),
    chat_model=os.getenv("ACE_CHAT_MODEL", "gemini-1.5-flash"),
    db_path=DB_PATH,
    chroma_dir=CHROMA_DIR,
    raw_data_dir=RAW_DATA_DIR,
    text_data_dir=TEXT_DATA_DIR,
)


def require_api_key() -> str:
    """Return the Gemini API key, or raise a clear error if it is missing."""
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env and add your key."
        )
    return settings.gemini_api_key