# Python RAG Project

## Overview
This directory contains the Python version of the RAG (Retrieval-Augmented Generation) project.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -e .
   ```

2. **Configure Environment:**
   Create a `.env` file in the root directory and add your Gemini API key:
   ```ini
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Run the application (single question):**
   ```bash
   python python/main.py --question "Ali Haydar Özer'in maili nedir?"
   ```

4. **Run the application (multiple questions / batch):**

   You can provide multiple questions by repeating the `-q/--question` flag.
   Each `-q` will be processed and an answer printed for each question.

   Example (PowerShell):
   ```powershell
   python python/main.py -q "İlk sorum nedir?" -q "İkinci sorum nedir?"
   ```

   The program will detect multiple questions and run them in batch, printing
   a separator and the corresponding answer for each provided question.

5. **Run tests:**
   ```bash
   pytest python/tests/
   ```

## Project Structure

```
python/
├── rag/                    # Main package
│   ├── answer/            # Answer generation
│   ├── chunker/           # Text chunking
│   ├── config/            # Configuration
│   ├── detector/          # Intent detection
│   ├── llm/               # LLM integration
│   ├── model/             # Data models
│   ├── orchestrator/      # Pipeline orchestration
│   ├── reranker/          # Result reranking
│   ├── retriever/         # Document retrieval
│   ├── store/             # Data storage
│   ├── tracer/            # Logging & tracing
│   ├── utility/           # Utilities
│   └── writer/            # Query writing
├── tests/                 # Unit tests
├── resources/             # Configuration & data
└── main.py               # Entry point
```

## Features

- **Intent Detection**: Rule-based intent classification
- **Query Writing**: Heuristic query processing with stemming
- **Retrieval**: Keyword-based document retrieval
- **Reranking**: Phrase-aware result reranking
- **Answer Generation**: Template-based or Gemini LLM-based answer synthesis
- **Tracing**: JSONL-based execution logging

## Configuration

Edit `python/resources/config.json` to customize:
- Intent detection rules
- Query processing parameters
- Retrieval settings
- Reranking options
- LLM settings (model name, API key environment variable)

## Design Patterns

- **Strategy Pattern**: Pluggable components
- **Observer Pattern**: Trace bus
- **Factory Pattern**: Component creation
- **Template Method**: Pipeline execution
- **Adapter Pattern**: Answer agent

## GRASP Principles

- **Controller**: `RagOrchestrator`
- **Pure Fabrication**: `Pipeline`
- **Information Expert**: Each component
- **Low Coupling**: Interface-based
- **High Cohesion**: Focused modules
