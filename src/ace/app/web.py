"""Streamlit chat interface for Ace.

    streamlit run src/ace/app/web.py
"""
from __future__ import annotations

import streamlit as st
from google.genai import types

from ace.llm.agent import chat

st.set_page_config(page_title="Ace", page_icon="🎾")
st.title("🎾 Ace")
st.caption("A tennis assistant that answers from real ATP match data.")

if "history" not in st.session_state:
    st.session_state.history = []
if "display" not in st.session_state:
    st.session_state.display = []

for msg in st.session_state.display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

if prompt := st.chat_input("Ask about a player, a matchup, the data..."):
    st.session_state.display.append({"role": "user", "text": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.history.append(
        types.Content(role="user", parts=[types.Part(text=prompt)])
    )
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st.session_state.history = chat(st.session_state.history)
            answer = st.session_state.history[-1].parts[0].text
        st.markdown(answer)

    st.session_state.display.append({"role": "assistant", "text": answer})