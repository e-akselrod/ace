"""Tool dispatch: run the real Python function the model asked for.

The model returns a tool name and arguments. This maps that name to the actual
query function and calls it. Keeping this in one place means adding a new tool
is just adding a line to the registry.
"""
from __future__ import annotations

from typing import Any, Callable

from ace.tools.queries import player_win_count, total_matches

REGISTRY: dict[str, Callable[..., Any]] = {
    "player_win_count": player_win_count,
    "total_matches": total_matches,
}

def run_tool(name: str, args: dict[str, Any]) -> Any:
    """Look up a tool by name and call it with the given arguments."""
    if name not in REGISTRY:
        raise ValueError(f"Unknown tool: {name}")
    func = REGISTRY[name]
    return func(**args)