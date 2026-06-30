"""Tool definitions: descriptions of the query functions for the model.

The model does not see the Python code. It sees these declarations, the name,
a plain-English description, and the inputs each function expects, and uses them
to decide which function to call and with what arguments.
"""
from __future__ import annotations

from google.genai import types

player_win_count_decl = types.FunctionDeclaration(
    name="player_win_count",
    description="Get the total number of matches a tennis player has won. "
                "Use this for questions about a player's career wins.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "name": types.Schema(
                type=types.Type.STRING,
                description="The player's full name, e.g. 'Novak Djokovic'.",
            ),
        },
        required=["name"],
    ),
)

total_matches_decl = types.FunctionDeclaration(
    name="total_matches",
    description="Get the total number of tennis matches in the database. "
                "Use this for questions about how much data is available.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={},
    ),
)

ALL_TOOLS = [player_win_count_decl, total_matches_decl]