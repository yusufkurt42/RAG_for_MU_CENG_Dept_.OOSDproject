# System Architecture

This document describes the architecture and design of the RAG System for Marmara University's Computer Engineering Department.

## Overview

The system follows a modular architecture with clear separation of concerns. It implements the Retrieval-Augmented Generation (RAG) pattern, combining document retrieval with language model generation.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User                                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ Query
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                     Main Application                         │
│                       (main.py)                             │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      RAG System                             │
│                   (rag_system.py)                           │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Document   │  │    Vector    │  │    Gemini    │    │
│  │  Processor   │  │    Store     │  │  Generator   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────────────────────────────────────┘
                  │                │                │
                  │                │                │
                  ▼                ▼                ▼
         ┌───────────────┐ ┌──────────────┐ ┌────────────┐
         │     Data      │ │   ChromaDB   │ │   Gemini   │
         │   Directory   │ │   (Vector)   │ │    API     │
         └───────────────┘ └──────────────┘ └────────────┘
```

## Components

### 1. Configuration Module (config.py)

**Purpose**: Centralized configuration management

**Responsibilities**:
- Load environment variables from .env file
- Provide configuration values to other modules
- Validate required settings

**Key Features**:
- Environment variable defaults
- Configuration validation
- Type-safe access to settings

**Configuration Parameters**:
- `GOOGLE_API_KEY`: API key for Gemini
- `CHROMA_PERSIST_DIRECTORY`: Database storage location
- `COLLECTION_NAME`: Vector collection name
- `EMBEDDING_MODEL`: Model for generating embeddings
- `GEMINI_MODEL`: Model for text generation
- `TOP_K_RESULTS`: Number of documents to retrieve

### 2. Document Processor (document_processor.py)

**Purpose**: Handle document loading and preprocessing

**Responsibilities**:
- Load documents from filesystem
- Chunk documents into manageable pieces
- Maintain document metadata

**Key Features**:
- Configurable chunk size and overlap
- Smart chunking at sentence boundaries
- Metadata preservation

**Methods**:
- `load_documents_from_directory()`: Load all .txt files
- `chunk_text()`: Split text with overlap
- `process_documents()`: Full processing pipeline

**Design Decisions**:
- Chunk size: 500 characters (balance between context and retrieval)
- Overlap: 50 characters (maintain continuity)
- Break at sentence boundaries (preserve semantic units)

### 3. Vector Store (vector_store.py)

**Purpose**: Manage document embeddings and similarity search

**Responsibilities**:
- Store document embeddings
- Generate embeddings using Gemini
- Perform similarity search
- Manage ChromaDB collection

**Key Features**:
- Persistent storage with ChromaDB
- Automatic embedding generation
- Configurable retrieval parameters
- Collection management

**Methods**:
- `add_documents()`: Index documents with embeddings
- `search()`: Find relevant documents
- `get_collection_count()`: Statistics
- `clear_collection()`: Reset database

**Technology Choice**:
- **ChromaDB**: Lightweight, embedded vector database
  - No separate server required
  - Persistent storage
  - Fast similarity search

### 4. Gemini Generator (gemini_generator.py)

**Purpose**: Generate responses using Gemini API

**Responsibilities**:
- Create prompts with context
- Call Gemini API for generation
- Format and return responses

**Key Features**:
- Context-aware prompt engineering
- Source attribution
- Error handling

**Methods**:
- `generate_response()`: Main generation method
- `_build_context()`: Format retrieved documents
- `_create_prompt()`: Construct prompt for Gemini

**Prompt Engineering**:
```
System Instructions
    ↓
Context Documents (from retrieval)
    ↓
User Question
    ↓
Generation Instructions
```

### 5. RAG System (rag_system.py)

**Purpose**: Orchestrate the complete RAG pipeline

**Responsibilities**:
- Initialize all components
- Coordinate document loading
- Execute query pipeline
- Provide system statistics

**Methods**:
- `load_documents()`: Load and index documents
- `query()`: Execute RAG pipeline
- `add_document()`: Add single document
- `get_stats()`: System information

**Query Pipeline**:
```
1. Receive query
    ↓
2. Generate query embedding
    ↓
3. Retrieve similar documents (top K)
    ↓
4. Build context from documents
    ↓
5. Generate response with Gemini
    ↓
6. Return answer + metadata
```

### 6. Main Application (main.py)

**Purpose**: User interface and interaction

**Responsibilities**:
- Interactive command-line interface
- User input handling
- Display formatted results
- Error handling and user feedback

**Features**:
- Interactive loop
- Multiple commands (query, stats, help, exit)
- Environment validation
- Graceful error handling

## Data Flow

### Document Indexing Flow

```
1. Load .txt files from data/
    ↓
2. Read file contents
    ↓
3. Chunk into smaller pieces
    ↓
4. Generate embeddings with Gemini
    ↓
5. Store in ChromaDB
    ↓
6. Ready for queries
```

### Query Processing Flow

```
1. User enters query
    ↓
2. Generate query embedding (Gemini)
    ↓
3. Search ChromaDB for similar documents
    ↓
4. Retrieve top K most relevant chunks
    ↓
5. Build context from chunks
    ↓
6. Create prompt with context + query
    ↓
7. Send to Gemini for generation
    ↓
8. Receive and format response
    ↓
9. Display to user
```

## Technology Stack

### Core Technologies

1. **Python 3.8+**: Primary language
2. **Google Gemini API**: Embeddings and generation
3. **ChromaDB**: Vector database
4. **LangChain**: LLM framework utilities

### Key Libraries

- `google-generativeai`: Official Gemini SDK
- `chromadb`: Vector database
- `python-dotenv`: Environment management
- `numpy`: Numerical operations

## Design Patterns

### 1. Facade Pattern
- `RAGSystem` provides simple interface to complex subsystems
- Hides complexity of vector search and generation

### 2. Strategy Pattern
- Different embedding and generation models can be configured
- Pluggable components

### 3. Factory Pattern
- Collection creation in VectorStore
- Model initialization

## Security Considerations

### API Key Management
- Never commit .env file
- Use environment variables
- Validate before use

### Input Validation
- Query sanitization
- File path validation
- Error handling

### Data Privacy
- Local document storage
- No data sent except to Gemini API
- Respect API usage limits

## Performance Considerations

### Embedding Generation
- Batch processing when possible
- Cache embeddings in ChromaDB
- Use efficient models

### Retrieval
- Index optimization
- Configurable top K
- Fast similarity search with ChromaDB

### Generation
- Single API call per query
- Reasonable context length
- Error recovery

## Scalability

### Current Limitations
- Single-machine deployment
- Synchronous processing
- Limited by API rate limits

### Future Improvements
- Batch query processing
- Async API calls
- Distributed vector store
- Caching layer

## Error Handling

### Levels of Error Handling

1. **Configuration Level**
   - Validate API key
   - Check file paths
   - Verify settings

2. **Processing Level**
   - File reading errors
   - Embedding failures
   - Database errors

3. **API Level**
   - Network timeouts
   - Rate limiting
   - Invalid responses

4. **User Level**
   - Clear error messages
   - Recovery suggestions
   - Graceful degradation

## Monitoring and Logging

### Current Logging
- Console output for operations
- Error messages
- Statistics display

### Potential Enhancements
- Structured logging
- Performance metrics
- Usage analytics
- Error tracking

## Testing Strategy

### Unit Tests
- Document processor chunking
- Configuration validation
- Utility functions

### Integration Tests
- Vector store operations
- End-to-end query flow
- Document loading

### Manual Testing
- Example queries
- Edge cases
- Error scenarios

## Deployment

### Local Development
```bash
1. Clone repository
2. Install dependencies
3. Configure .env
4. Run main.py
```

### Production Considerations
- Virtual environment
- Process management
- Log rotation
- Backup strategy
- API key rotation

## Maintenance

### Regular Tasks
- Update dependencies
- Monitor API changes
- Review logs
- Backup database

### Document Updates
- Add new .txt files to data/
- Restart system to reindex
- Or use add_document() API

## Future Enhancements

### Potential Features
1. Web interface
2. REST API
3. Multi-language support
4. Document format support (PDF, DOCX)
5. Real-time updates
6. User authentication
7. Query history
8. Feedback mechanism
9. A/B testing
10. Advanced analytics

### Technical Improvements
1. Async processing
2. Caching layer
3. Load balancing
4. Horizontal scaling
5. Advanced retrieval (hybrid search)
6. Fine-tuned models
7. Better chunking strategies
8. Query optimization
