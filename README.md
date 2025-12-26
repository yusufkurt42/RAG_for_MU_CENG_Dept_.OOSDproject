Burak İşgören: 150122071
Eren Osman: 150123054
Sabri Yıldız: 150122025
Şükrü Yücel: 150122040
Yusuf Kurt: 150123078

Commands: Instructions on how to run the project from the command line (e.g., java -jar rag.jar ...).

Config Schema: Documentation explaining the structure and options available in your YAML/JSON configuration files.

Directory Layout: An overview of the project's folder structure.

Unit Tests: Information regarding your test suite, specifically verifying that you have "26 tests across 24 classes".

# RAG Project - Python Version

This is a Python port of the Java RAG (Retrieval-Augmented Generation) system.

## Project Structure

```
python/
├── rag/
│   ├── answer/          # Answer generation components
│   ├── chunker/         # Text chunking implementations
│   ├── config/          # Configuration management
│   ├── detector/        # Intent detection
│   ├── model/           # Data models
│   ├── orchestrator/    # Pipeline orchestration
│   ├── reranker/        # Result reranking
│   ├── retriever/       # Document retrieval
│   ├── store/           # Data persistence
│   ├── tracer/          # Logging and tracing
│   ├── utility/         # Utility functions
│   └── writer/          # Query writing
├── tests/               # Unit tests
└── resources/           # Configuration and data files
```

## Installation

```bash
pip install -e .
```

## Running the Application

```bash
python python/main.py --question "Your question here"
```

### Command Line Options

- `--config`: Path to configuration file (default: `resources/config.json`)
- `--chunks`: Path to chunks file (default: `resources/chunks.json`)
- `--question` or `-q`: Question to ask the RAG system

## Running Tests

```bash
pytest python/tests/
```

## Configuration

The system uses JSON configuration files in the `resources/` directory:

- `config.json`: Main configuration file
- `chunks.json`: Pre-chunked document data
- `keyword_index.json`: Keyword index for retrieval
- `rules.json`: Intent detection rules

## Design Patterns Used

- **Strategy Pattern**: Different implementations for chunking, retrieval, etc.
- **Observer Pattern**: Trace bus for logging events
- **Factory Pattern**: Component creation
- **Template Method**: Pipeline execution flow
- **Adapter Pattern**: Answer agent integration

## GRASP Principles

- **Controller**: RagOrchestrator coordinates the workflow
- **Pure Fabrication**: Pipeline handles stage execution mechanics
- **Information Expert**: Each component manages its own data
- **Low Coupling**: Interfaces define component boundaries
- **High Cohesion**: Each module has focused responsibilities