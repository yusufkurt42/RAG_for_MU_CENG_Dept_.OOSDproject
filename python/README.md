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

3. **Run the application:**
   ```bash
   python python/main.py --question "Ali Haydar Özer'in maili nedir?"
   ```

4. **Run tests:**
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
