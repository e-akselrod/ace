# Ace

A tennis intelligence assistant. Ask it about tennis and it answers from real data: factual questions trigger a function call against a database of 60,000+ ATP matches, so answers come from records instead of guesses. A retrieval layer for context and a generation layer for previews are planned (see the roadmap).

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-in%20development-orange)

> Status: in active development. The roadmap below shows what is built and what is next.

## Demo

![Ace answering tennis questions from real ATP match data](assets/demo.png)

## Overview

Most chatbots answer tennis questions from memory and quietly get the numbers wrong. Ace is built so it does not have to guess: factual questions are answered from the database, and the design extends to context and narrative as the retrieval layer is added.

- Tool use for facts (built). A question like "how many matches has Djokovic won?" triggers a function call against a local SQLite database of real ATP results, so the answer comes from real numbers, not the model's memory.
- Retrieval for context (planned). Questions like "what made the 2008 Wimbledon final special?" will pull relevant passages from an embedded text corpus and answer from them. This is retrieval-augmented generation (RAG).
- Generation (planned). Match previews, career summaries, and scouting reports.

## Architecture

    question
       |
       v
    [ Gemini ] --calls--> stats tools --> SQLite (ATP matches)
        |      --asks-->  retriever*   --> Chroma (embedded text)
        v
    grounded answer

    * the retrieval layer is planned (see roadmap)

## Tech stack

- Python 3.10+
- Google Gemini API for chat and tool calling
- SQLite for the match database
- Streamlit for the web interface
- pytest for tests

Planned: sentence-transformers and Chroma for the retrieval (RAG) layer.

## Getting started

Requires Python 3.10 or later, and a free Google Gemini API key from https://aistudio.google.com/apikey.

    git clone https://github.com/e-akselrod/ace.git
    cd ace
    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
    pip install -e ".[dev]"
    python -m ace.ingest.download    # download ATP match data into data/raw

Add your key to a file named .env in the project root:

    GEMINI_API_KEY=your_key_here

Then launch the chat app:

    streamlit run src/ace/app/web.py

## Roadmap

- [x] Project scaffold and configuration
- [x] Match-data download
- [x] Load 60,000+ matches into SQLite
- [x] Query layer and tool calling (Gemini decides, the database answers)
- [x] Conversational chat with memory
- [x] Streamlit web interface and demo
- [ ] More stats tools: head-to-head, surface records, titles
- [ ] RAG over a tennis text corpus
- [ ] Generative previews and scouting reports
- [ ] Tests and CI
- [ ] Error handling and polish

## Project structure

    src/ace/
      config.py     paths, settings, model defaults
      ingest/       download match data and load it into SQLite
      tools/        query functions and their tool definitions
      llm/          Gemini client and the tool-calling agent loop
      app/          Streamlit chat interface

    (a retrieval/ package for the RAG layer is planned)

## Data and licensing

Match data comes from the Tennismylife TML-Database, an ATP results dataset in the column format popularised by Jeff Sackmann and sourced from the official ATP site. It is used here for educational and analytical purposes with attribution, under a Creative Commons Attribution-NonCommercial-ShareAlike license. The data is downloaded at runtime and is not redistributed in this repository.

## License

The code in this project is released under the MIT License. See the LICENSE file.

## Acknowledgments

- Match data: the Tennismylife TML-Database and Jeff Sackmann's tennis data format.