"""Central configuration for the ACE project.

"Loads environment variables and defines the paths and model defaults used
across the project. Import ``settings`` from here rather than reading
``os.environ`` in several different places.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Define the project root and data directories
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
TEXT_DATA_DIR = DATA_DIR / "text"
DB_PATH = DATA_DIR / "ace.db"
CHROMA_DB_DIR = DATA_DIR / "chroma"

@dataclass(frozen=True)
class Settings:
    """Run-time settings, loaded from environment variables."""

    anthropics_api_key: str | None
    chat_model: str
    db_path: Path
    chroma_dir: Path
    raw_data_dir: Path
    text_data_dir: Path

settings = Settings(
    anthropics_api_key=os.getenv("ANTHROPIC_API_KEY"),
    chat_model=os.getenv("ACE_CHAT_MODEL", "claude-sonnet-4-6"),
    db_path = DB_PATH,
    chroma_dir = CHROMA_DB_DIR,
    raw_data_dir = RAW_DATA_DIR,
    text_data_dir = TEXT_DATA_DIR,
)

def require_api_key() -> str:
    """Get the API key from settings, raising an error if it's not set."""
    if not settings.anthropics_api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set in the environment. Copy .env.example to .env and add your key."
            )
    return settings.anthropics_api_key