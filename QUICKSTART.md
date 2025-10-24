# Quick Start Guide

Get started with the RAG System in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- A Google API key for Gemini API

## Step 1: Get Your API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yusufkurt42/RAG_System_for_MarmaraUniversityCENG_Dept_.OOSDproject.git
cd RAG_System_for_MarmaraUniversityCENG_Dept_.OOSDproject

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
```

## Step 3: Configure

Edit the `.env` file and add your API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

## Step 4: Run!

```bash
python main.py
```

## Your First Query

Once the system starts, try these queries:

```
> What is the Computer Engineering Department?

> What courses are taught in the first year?

> Who are the faculty members?

> What research areas are available?
```

## Example Session

```
======================================================================
RAG System for Marmara University Computer Engineering Department
======================================================================

Initializing RAG system...
Loading documents from /home/user/project/data...
Loaded 5 documents
Created 32 chunks
Indexed documents. Total documents in store: 32

RAG system ready!

Available Commands:
  query <question>  - Ask a question about the department
  stats             - Show system statistics
  help              - Show this help message
  exit              - Exit the application


> What courses are in the first year curriculum?

Processing query: What courses are in the first year curriculum?
Retrieved 3 relevant documents

======================================================================
ANSWER:
======================================================================
Based on the curriculum document, the first year courses include:

Fall Semester:
- Introduction to Computer Engineering and Programming I
- Calculus I
- Physics I
- Chemistry
- Technical English I
- Atatürk's Principles and History of Turkish Revolution I

Spring Semester:
- Introduction to Computer Engineering and Programming II
- Calculus II
- Physics II
- Linear Algebra
- Technical English II
- Atatürk's Principles and History of Turkish Revolution II

These courses provide a strong foundation in mathematics, science, and 
programming for computer engineering students.
======================================================================
Based on 3 retrieved documents
======================================================================

> exit
Thank you for using the RAG system. Goodbye!
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `<question>` | Ask any question (just type it) |
| `query <question>` | Explicitly query (alternative) |
| `stats` | Show system statistics |
| `help` | Display help message |
| `exit` or `quit` | Exit the application |

## Common Questions

### Q: Where does the data come from?
**A:** The system uses documents from the `data/` directory. You can add more `.txt` files there.

### Q: How do I add new information?
**A:** Simply add new `.txt` files to the `data/` directory and restart the application.

### Q: Can I use this for other departments?
**A:** Yes! Replace the documents in the `data/` directory with information about your department.

### Q: How accurate are the answers?
**A:** The system uses Google's Gemini model and only provides information from the loaded documents.

### Q: Is my data private?
**A:** Documents are stored locally. Only queries and relevant document chunks are sent to Gemini API.

## Troubleshooting

### "GOOGLE_API_KEY is not set"
- Make sure you created the `.env` file
- Check that your API key is correctly pasted
- No extra spaces or quotes around the key

### "No module named 'chromadb'"
- Run: `pip install -r requirements.txt`
- Make sure you're using Python 3.8+

### "No documents loaded"
- Check that `.txt` files exist in the `data/` directory
- Verify file permissions (should be readable)

### Slow responses
- First query is slower (loading model)
- Check your internet connection
- Gemini API might be experiencing delays

## Next Steps

1. **Read the Full Documentation**
   - See `README.md` for comprehensive information
   - Check `docs/USAGE.md` for more examples
   - Read `docs/ARCHITECTURE.md` for technical details

2. **Customize Your System**
   - Add your own documents
   - Modify chunk size in `src/document_processor.py`
   - Adjust retrieval parameters in `.env`

3. **Explore the API**
   - Use the Python API for programmatic access
   - See `docs/USAGE.md` for code examples
   - Build your own applications on top

4. **Contribute**
   - Report issues on GitHub
   - Suggest improvements
   - Share your use cases

## Tips for Better Results

1. **Be specific** in your questions
   - ✓ "What courses are in third year?"
   - ✗ "Tell me about courses"

2. **Use natural language** - the system understands conversational queries

3. **Ask follow-up questions** - you can have a conversation

4. **Check stats** regularly to ensure documents are loaded

5. **Restart** after adding new documents

## Getting Help

- Read the documentation in `docs/`
- Check `README.md` for detailed information
- Open an issue on GitHub
- Review example queries in `docs/USAGE.md`

## Success Indicators

You'll know the system is working when:
- ✓ Documents load without errors
- ✓ Stats show document count > 0
- ✓ Queries return relevant answers
- ✓ Answers cite source documents

Enjoy using your RAG system! 🚀
