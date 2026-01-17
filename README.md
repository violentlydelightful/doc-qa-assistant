# Document Q&A Assistant

An AI-powered tool for asking questions about uploaded documents. Upload a PDF, Word doc, or text file and get instant answers about its contents.

## The Problem

Reading through long documents to find specific information is time-consuming. Whether it's a contract, research paper, or policy document, finding answers often means manual searching and reading.

## The Solution

This tool lets you:
1. Upload any document (PDF, DOCX, TXT, MD)
2. Ask natural language questions
3. Get AI-powered answers based on the document content

## Features

- **Multi-format support**: PDF, Word documents, plain text, Markdown
- **Conversational interface**: Ask follow-up questions naturally
- **Context-aware answers**: AI only answers based on document content
- **Works offline**: Demo mode available without API key
- **Clean UI**: Modern, responsive chat interface

## Tech Stack

- **Backend**: Python, Flask
- **AI**: OpenAI GPT (with fallback demo mode)
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: Vanilla JavaScript, CSS

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# (Optional) Set OpenAI API key for full AI capabilities
export OPENAI_API_KEY=your-key-here

# Run the app
python run.py

# Open in browser
open http://localhost:5001
```

## How It Works

1. **Document Upload**: File is parsed and text is extracted
2. **Text Processing**: Content is chunked for efficient processing
3. **Question Handling**: Your question + document context sent to AI
4. **Response**: AI generates answer based only on document content

## Project Structure

```
doc-qa-assistant/
├── app/
│   ├── __init__.py           # App factory
│   ├── routes.py             # API endpoints
│   ├── document_processor.py # Text extraction & chunking
│   ├── ai_service.py         # LLM integration (pluggable)
│   └── templates/
│       └── index.html        # Chat interface
├── static/
│   └── style.css             # Styling
├── uploads/                   # Temporary file storage
├── config.py                  # Configuration
├── run.py                     # Entry point
└── requirements.txt           # Dependencies
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main chat interface |
| `/upload` | POST | Upload a document |
| `/ask` | POST | Ask a question about uploaded doc |
| `/documents` | GET | List all uploaded documents |
| `/document/<id>` | GET | Get document details |

## Architecture Decisions

### Pluggable AI Provider
The `ai_service.py` module uses an abstract base class pattern, making it easy to swap LLM providers:

```python
# Currently supports
provider = get_ai_provider("openai")  # GPT-3.5/4
provider = get_ai_provider("mock")    # Demo mode
provider = get_ai_provider("auto")    # Auto-detect
```

### Document Chunking
Large documents are split into overlapping chunks to stay within token limits while maintaining context.

### Demo Mode
Without an API key, the app falls back to simple keyword matching. This allows the project to be demonstrated without incurring API costs.

## Future Enhancements

- Vector embeddings for semantic search
- Support for more file formats (HTML, EPUB)
- Conversation history persistence
- Multiple document comparison
- Source highlighting in answers

## Use Cases

- **Contract Review**: "What are the termination clauses?"
- **Research**: "What methodology did this study use?"
- **Policy Analysis**: "What's the policy on remote work?"
- **Meeting Notes**: "What action items were assigned?"

---

*Built as a portfolio project demonstrating AI integration and practical tool development.*
