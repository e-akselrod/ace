"""Streamlit chat interface for Ace.

A simple chat webpage on top of the agent''s chat() function. Run with:

    streamlit run src/ace/app/web.py
"""
from __future__ import annotations

import streamlit as st
from google.genai import types

from ace.llm.agent import chat, ModelError

st.set_page_config(page_title="Ace", page_icon="🎾")
st.title("🎾 Ace")
st.caption("A tennis assistant that answers from real ATP match data.")

# Two copies of the conversation live in session state so they survive between
# messages: the full history the model needs (with tool calls), and a clean
# display version (just user and assistant text).
if "history" not in st.session_state:
    st.session_state.history = []
if "display" not in st.session_state:
    st.session_state.display = []

# Redraw the visible conversation on each run.
for msg in st.session_state.display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# The input box at the bottom.
if prompt := st.chat_input("Ask about a player, a matchup, the data..."):
    # Show and record the user message.
    st.session_state.display.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build the next history, but only commit it to session state on success.
    pending = st.session_state.history + [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                updated = chat(pending)
                answer = updated[-1].parts[0].text
            st.markdown(answer)
            st.session_state.history = updated
            st.session_state.display.append({"role": "assistant", "text": answer})
        except ModelError as exc:
            # The model was unavailable. Show a calm message instead of crashing,
            # and leave the history unchanged so the user can just try again.
            st.error(str(exc))
