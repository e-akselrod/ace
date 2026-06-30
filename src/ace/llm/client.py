"""Talking to the language model (Gemini).

A thin wrapper around the google-genai client. The rest of the project calls
``generate`` and does not need to know the provider details. Swapping models or
providers later means changing only this file.
"""
from __future__ import annotations

from google import genai

from ace.config import require_api_key, settings

_client = genai.Client(api_key=require_api_key())

def generate(prompt: str) -> str:
    """Send a prompt to the model and return its text reply."""
    response = _client.models.generate_content(
        model=settings.chat_model,
        contents=prompt,
    )
    return response.text