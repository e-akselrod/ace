"""The agent loop: let the model answer questions using tools.

Flow:
  1. Send the user's question plus the tool menu to the model.
  2. If the model asks to call a tool, run it and send the result back.
  3. Repeat until the model returns a normal text answer.

This is what makes Ace accurate: facts come from the database via tools, and the
model only phrases the final answer.
"""
from __future__ import annotations

from google import genai
from google.genai import types

from ace.config import require_api_key, settings
from ace.tools.definitions import ALL_TOOLS
from ace.tools.dispatch import run_tool

_client = genai.Client(api_key=require_api_key())

SYSTEM_INSTRUCTION = (
    "You are Ace, a tennis expert assistant. When a question needs match facts "
    "or statistics, use the provided tools to look up real data instead of "
    "guessing. Answer clearly and concisely."
)

_tools = types.Tool(function_declarations=ALL_TOOLS)
_config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[_tools],
)

def ask(question: str) -> str:
    """Answer a question, using tools when the model decides it needs them."""
    contents = [
        types.Content(role="user", parts=[types.Part(text=question)]),
    ]

    while True:
        response = _client.models.generate_content(
            model=settings.chat_model,
            contents=contents,
            config=_config,
        )

        function_calls = response.function_calls
        if not function_calls:
            return response.text

        contents.append(response.candidates[0].content)

        for call in function_calls:
            result = run_tool(call.name, dict(call.args))
            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": result},
                        )
                    ],
                )
            )

def chat(history: list[types.Content]) -> list[types.Content]:
    """Continue a conversation"""

    while True:
        response = _client.models.generate_content(
            model=settings.chat_model,
            contents=history,
            config=_config,
        )

        function_calls = response.function_calls
        if not function_calls:
            history.append(response.candidates[0].content)
            return history

        history.append(response.candidates[0].content)
        for call in function_calls:
            result = run_tool(call.name, dict(call.args))
            history.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": result},
                        )
                    ],
                )
            )