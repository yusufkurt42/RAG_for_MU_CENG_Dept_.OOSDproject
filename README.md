# RAG System for Marmara University Computer Engineering Department

A Retrieval-Augmented Generation (RAG) system built with Google's Gemini API to answer questions about Marmara University's Computer Engineering Department.

## Overview

This system uses RAG architecture to provide accurate and contextual answers about the Computer Engineering Department at Marmara University. It combines document retrieval with Gemini's language generation capabilities to deliver informative responses based on department documentation.

## Features

- **Document Processing**: Automatically processes and chunks documents for efficient retrieval
- **Vector-based Search**: Uses embeddings and ChromaDB for semantic similarity search
- **Gemini Integration**: Leverages Google's Gemini API for both embeddings and text generation
- **Interactive Interface**: Command-line interface for easy querying
- **Extensible Architecture**: Easy to add new documents and expand the knowledge base

## Architecture

The system consists of several key components:

1. **Document Processor**: Loads and chunks text documents into manageable pieces
2. **Vector Store**: Uses ChromaDB to store and search document embeddings
3. **Gemini Generator**: Generates contextual responses using Gemini API
4. **RAG System**: Orchestrates the entire retrieval and generation pipeline

## Installation

### Prerequisites

- Python 3.8 or higher
- Google API key for Gemini API

### Setup Steps

1. Clone the repository:
```bash
git clone https://github.com/yusufkurt42/RAG_System_for_MarmaraUniversityCENG_Dept_.OOSDproject.git
cd RAG_System_for_MarmaraUniversityCENG_Dept_.OOSDproject
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### Getting a Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key and paste it into your `.env` file

## Usage

### Starting the Application

Run the main application:
```bash
python main.py
```

### Interactive Commands

Once the application starts, you can use the following commands:

- **Ask a question**: Simply type your question and press Enter
  ```
  > What courses are offered in the first year?
  ```

- **View statistics**: Check system information
  ```
  > stats
  ```

- **Get help**: Show available commands
  ```
  > help
  ```

- **Exit**: Quit the application
  ```
  > exit
  ```

### Example Queries

Here are some example questions you can ask:

1. "What is the Computer Engineering Department at Marmara University?"
2. "What courses are available in the curriculum?"
3. "Who are the faculty members?"
4. "What research areas are covered in the department?"
5. "What labs and facilities are available?"
6. "How many ECTS credits are required to graduate?"
7. "What are the graduation requirements?"
8. "Tell me about the AI and Machine Learning lab"
9. "What elective courses can I take?"
10. "Who is the department head?"

## Project Structure

```
.
├── src/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration management
│   ├── document_processor.py # Document loading and chunking
│   ├── vector_store.py       # Vector database operations
│   ├── gemini_generator.py   # Gemini API integration
│   └── rag_system.py         # Main RAG system orchestration
├── data/
│   ├── department_overview.txt
│   ├── curriculum.txt
│   ├── faculty.txt
│   └── labs_facilities.txt
├── main.py                   # Main application entry point
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment configuration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Adding New Documents

To expand the knowledge base:

1. Add new `.txt` files to the `data/` directory
2. Restart the application to load the new documents

Alternatively, use the programmatic API:
```python
from src.rag_system import RAGSystem

rag = RAGSystem()
rag.add_document(content="Your document content", source="document_name.txt")
```

## Configuration

The system can be configured through environment variables in the `.env` file:

- `GOOGLE_API_KEY`: Your Google API key (required)
- `CHROMA_PERSIST_DIRECTORY`: Directory for vector database storage
- `COLLECTION_NAME`: Name of the document collection
- `EMBEDDING_MODEL`: Gemini embedding model to use
- `GEMINI_MODEL`: Gemini generation model to use
- `TOP_K_RESULTS`: Number of documents to retrieve for each query

## Technical Details

### Document Processing

Documents are processed in the following way:
1. Loaded from text files
2. Chunked into smaller pieces (default 500 characters with 50 character overlap)
3. Embeddings generated using Gemini's embedding model
4. Stored in ChromaDB for efficient retrieval

### Retrieval Process

When a query is received:
1. Query is converted to an embedding vector
2. Similar documents are retrieved using cosine similarity
3. Top K most relevant documents are selected
4. Retrieved documents are used as context for generation

### Generation Process

The system creates a prompt that includes:
1. System instructions for the AI assistant
2. Retrieved context documents
3. User's question
4. Instructions for generating accurate responses

## Dependencies

Main dependencies include:
- `google-generativeai`: Google's Gemini API client
- `chromadb`: Vector database for embeddings
- `langchain`: Framework for LLM applications
- `python-dotenv`: Environment variable management

See `requirements.txt` for the complete list.

## Troubleshooting

### API Key Issues

If you see authentication errors:
- Verify your API key is correct in `.env`
- Check that your API key has Gemini API access enabled
- Ensure you have internet connectivity

### Document Loading Issues

If documents aren't loading:
- Check that `.txt` files are in the `data/` directory
- Verify file encoding is UTF-8
- Ensure files have read permissions

### ChromaDB Issues

If you encounter database errors:
- Delete the `chroma_db/` directory and restart
- Check available disk space
- Verify write permissions in the project directory

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the terms included in the LICENSE file.

## Acknowledgments

- Marmara University Computer Engineering Department
- Google Gemini API
- ChromaDB
- LangChain community

## Contact

For questions or support, please open an issue on GitHub.