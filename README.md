# Ace

A tennis intelligence assistant. Ask it about tennis and it answers in two ways: it queries a real match database for exact facts, and it retrieves from a text corpus for context and narrative. It can also generate match previews and scouting reports.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-in%20development-orange)

> Status: in active development. The roadmap below shows what is built and what is next.

## Overview

Most chatbots answer tennis questions from memory and quietly get the numbers wrong. Ace is built so it never has to guess: factual questions are answered from data, and contextual questions are answered from sourced text.

- Tool use for facts. A question like "what is the Federer vs Nadal head-to-head on clay?" triggers a function call against a local SQLite database of real ATP results, so the answer comes from real numbers.
- Retrieval for context. A question like "what made the 2008 Wimbledon final special?" pulls relevant passages from an embedded text corpus and answers from them. This is retrieval-augmented generation (RAG).
- Generation. Match previews, career summaries, and scouting reports for any matchup.

## Architecture

    question
       |
       v
    [ Claude ] --calls--> stats tools --> SQLite (ATP matches)
        |      --asks-->  retriever   --> Chroma (embedded text)
        v
    grounded answer

## Tech stack

- Python 3.10+
- Anthropic Claude API for chat, tool use, and generation
- sentence-transformers for local embeddings (Voyage AI as an optional upgrade)
- Chroma as the vector store
- SQLite for structured match data
- Streamlit for the chat interface
- pytest for tests

## Getting started

Requires Python 3.10 or later.

    git clone https://github.com/e-akselrod/ace.git
    cd ace
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
    pip install -e ".[dev]"
    python -m ace.ingest.download    # downloads ATP match data into data/raw

Usage instructions for chatting with Ace will be added once the chat interface lands (see the roadmap).

## Roadmap

- [x] Project scaffold and configuration
- [x] Match-data download
- [ ] Load match data into SQLite
- [ ] Stats tools: head-to-head, player summaries, surface records
- [ ] Claude API with tool use (first working chatbot)
- [ ] RAG over a tennis text corpus
- [ ] Generative previews and scouting reports
- [ ] Streamlit chat interface and demo
- [ ] Evaluation harness and polish

## Project structure

    src/ace/
      config.py     paths, settings, model defaults
      ingest/       download data, load it, build the text corpus
      retrieval/    embeddings and vector search
      tools/        functions the model can call for stats
      llm/          Claude client, prompts, chat loop, generation
      app/          command line and Streamlit interfaces

## Data and licensing

Match data comes from the Tennismylife TML-Database, an ATP results dataset in the column format popularised by Jeff Sackmann and sourced from the official ATP site. It is used here for educational and analytical purposes with attribution, under a Creative Commons Attribution-NonCommercial-ShareAlike license. The data is downloaded at runtime and is not redistributed in this repository.

## License

The code in this project is released under the MIT License. See the LICENSE file.

## Acknowledgments

- Match data: the Tennismylife TML-Database and Jeff Sackmann's tennis data format.