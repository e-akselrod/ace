"""The agent loop: let the model answer questions using tools.

Flow:
  1. Send the conversation plus the tool menu to the model.
  2. If the model asks to call a tool, run it and send the result back.
  3. Repeat until the model returns a normal text answer.

If the model cannot be reached (rate limit, busy server, bad request), the raw
API error is translated into a ModelError with a clear, human-readable message,
so callers never see a traceback.
"""
from __future__ import annotations

from google import genai
from google.genai import errors as genai_errors
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


class ModelError(Exception):
    """Raised when the language model cannot be reached or fails to respond."""


def _friendly_message(exc: genai_errors.APIError) -> str:
    """Turn a raw API error into a calm, human-readable message."""
    code = getattr(exc, "code", None)
    if code == 429:
        return (
            "Ace has reached the free usage limit for now. "
            "Please wait a minute and try again."
        )
    if code == 503:
        return (
            "The model is busy at the moment. Please try again in a few seconds."
        )
    return "Ace could not reach the model right now. Please try again shortly."


def _call_model(contents: list[types.Content]):
    """Call the model once, translating any API error into a ModelError."""
    try:
        return _client.models.generate_content(
            model=settings.chat_model,
            contents=contents,
            config=_config,
        )
    except genai_errors.APIError as exc:
        raise ModelError(_friendly_message(exc)) from exc


def ask(question: str) -> str:
    """Answer a single question, using tools when the model decides it needs them."""
    contents: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=question)]),
    ]
    while True:
        response = _call_model(contents)
        if not response.function_calls:
            return response.text
        contents.append(response.candidates[0].content)
        for call in response.function_calls:
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
    """Continue a conversation, using tools when needed.

    Takes the conversation so far and returns a new list with the assistant's
    reply appended. The input is not modified, so if a call fails partway the
    caller's history stays clean and the user can simply try again.
    """
    convo = list(history)
    while True:
        response = _call_model(convo)
        if not response.function_calls:
            convo.append(response.candidates[0].content)
            return convo
        convo.append(response.candidates[0].content)
        for call in response.function_calls:
            result = run_tool(call.name, dict(call.args))
            convo.append(
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
