# Usage Examples

This document provides example queries and usage scenarios for the RAG System.

## Starting the Application

```bash
python main.py
```

## Example Query Session

```
======================================================================
RAG System for Marmara University Computer Engineering Department
======================================================================

Initializing RAG system...
Loading documents from /path/to/data...
Loaded 5 documents
Created 45 chunks
Indexed documents. Total documents in store: 45

RAG system ready!

Available Commands:
  query <question>  - Ask a question about the department
  stats             - Show system statistics
  help              - Show this help message
  exit              - Exit the application


> What is the Computer Engineering Department at Marmara University?

Processing query: What is the Computer Engineering Department at Marmara University?
Retrieved 3 relevant documents

======================================================================
ANSWER:
======================================================================
The Computer Engineering Department at Marmara University is one of the leading 
engineering departments in Turkey, founded in 1991. According to Document 1, 
it offers comprehensive education at both undergraduate and graduate levels...

======================================================================
Based on 3 retrieved documents
======================================================================
```

## Common Query Examples

### 1. General Information Queries

**Query**: "Tell me about the Computer Engineering Department"
- Returns overview, mission, and general information

**Query**: "What programs does the department offer?"
- Returns information about BS, MS, and PhD programs

**Query**: "What are the research areas in the department?"
- Lists all research areas like AI, ML, Networks, etc.

### 2. Curriculum Queries

**Query**: "What courses are taught in the first year?"
- Returns first-year curriculum details

**Query**: "What are the elective courses available?"
- Lists all elective course options

**Query**: "How many ECTS credits do I need to graduate?"
- Returns graduation requirements

**Query**: "What is the graduation project?"
- Explains the two-semester graduation project requirement

### 3. Faculty Queries

**Query**: "Who are the professors in the department?"
- Lists all faculty members with their titles

**Query**: "Who is the department head?"
- Returns current department head information

**Query**: "Who teaches artificial intelligence?"
- Returns faculty members in AI research area

**Query**: "What are the office hours for faculty?"
- Returns information about faculty availability

### 4. Facilities Queries

**Query**: "What labs are available for students?"
- Lists all research and general labs

**Query**: "Tell me about the AI and Machine Learning lab"
- Returns specific information about the AI lab

**Query**: "What software is available in the labs?"
- Lists all available software and tools

**Query**: "When are the computer labs open?"
- Returns operating hours

### 5. Admission Queries

**Query**: "How can I apply to the Computer Engineering program?"
- Returns admission requirements for different student types

**Query**: "What are the requirements for international students?"
- Specific information for international applicants

**Query**: "Are there scholarships available?"
- Lists scholarship opportunities

### 6. Student Life Queries

**Query**: "What student clubs are available?"
- Lists all student organizations

**Query**: "What is the Erasmus program?"
- Explains exchange opportunities

**Query**: "Where can I find internship opportunities?"
- Returns career services information

## Using the Python API

### Basic Usage

```python
from src.rag_system import RAGSystem

# Initialize the system
rag = RAGSystem()

# Load documents
rag.load_documents('./data')

# Query the system
result = rag.query("What courses are in the curriculum?")
print(result['answer'])
```

### Advanced Usage

```python
from src.rag_system import RAGSystem

# Initialize system
rag = RAGSystem()
rag.load_documents('./data')

# Custom retrieval parameters
result = rag.query(
    "What research areas are available?",
    top_k=5  # Retrieve more documents for context
)

# Access retrieved documents
for i, doc in enumerate(result['retrieved_documents'], 1):
    print(f"\nDocument {i}:")
    print(f"Source: {doc['metadata']['source']}")
    print(f"Distance: {doc['distance']}")
    print(f"Content: {doc['content'][:200]}...")

# Get system statistics
stats = rag.get_stats()
print(f"\nTotal documents: {stats['total_documents']}")
print(f"Model: {stats['model']}")
```

### Adding New Documents Programmatically

```python
from src.rag_system import RAGSystem

rag = RAGSystem()
rag.load_documents('./data')

# Add a new document
new_content = """
New information about a department event:
The Computer Engineering Department will host a Tech Summit on March 15, 2025.
Students and faculty are invited to present their research projects.
"""

rag.add_document(
    content=new_content,
    source="tech_summit_2025.txt"
)

# Now you can query about the new event
result = rag.query("When is the Tech Summit?")
print(result['answer'])
```

### Custom Configuration

```python
import os
os.environ['TOP_K_RESULTS'] = '5'
os.environ['GEMINI_MODEL'] = 'gemini-pro'

from src.rag_system import RAGSystem

rag = RAGSystem()
# System will use the custom configuration
```

## Batch Processing Queries

```python
from src.rag_system import RAGSystem

rag = RAGSystem()
rag.load_documents('./data')

questions = [
    "What is the department mission?",
    "Who are the faculty members?",
    "What labs are available?",
    "How do I apply?"
]

for question in questions:
    print(f"\n{'='*70}")
    print(f"Q: {question}")
    print('='*70)
    result = rag.query(question)
    print(result['answer'])
```

## Error Handling

```python
from src.rag_system import RAGSystem
from src.config import Config

try:
    # Validate configuration first
    Config.validate()
    
    rag = RAGSystem()
    rag.load_documents('./data')
    
    result = rag.query("Your question here")
    print(result['answer'])
    
except ValueError as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file")
    
except Exception as e:
    print(f"Error: {e}")
```

## Tips for Best Results

1. **Be Specific**: More specific questions get better answers
   - Good: "What courses are taught in the third year?"
   - Less good: "Tell me about courses"

2. **Use Natural Language**: The system understands natural questions
   - "What's the department's phone number?"
   - "How many professors work here?"
   - "Can you tell me about the AI lab?"

3. **Follow-up Questions**: You can ask related follow-up questions
   - First: "What is the curriculum?"
   - Then: "What about elective courses?"

4. **Check Statistics**: Use the `stats` command to verify documents are loaded

5. **Understand Context**: The system uses 3 documents by default for context
   - Increase `TOP_K_RESULTS` in .env for more context
   - More context = more comprehensive but potentially verbose answers

## Troubleshooting Common Issues

### No Documents Loaded
```
> stats
total_documents: 0
```
**Solution**: Check that .txt files are in the data/ directory

### API Key Error
```
Error: GOOGLE_API_KEY is not set
```
**Solution**: Create .env file with your API key

### Empty Responses
**Solution**: 
- Verify your API key is valid
- Check internet connectivity
- Ensure documents are properly loaded

### Slow Responses
**Solution**:
- Reduce TOP_K_RESULTS in configuration
- Check internet speed
- Consider chunking very large documents smaller
