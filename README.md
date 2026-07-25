# Chat with Your File

A local, offline-friendly Retrieval-Augmented Generation (RAG) app that lets you upload a document (PDF, TXT, or Markdown) and ask questions about it. All processing — embedding, retrieval, and chat — runs through a local Ollama server and a persistent ChromaDB vector store, so your files never leave your machine.

## Features

- Upload PDF, TXT, or Markdown files and index them into a local vector store.
- Ask natural-language questions and get answers grounded only in your document's content.
- Switch between locally available Ollama chat models.
- Minimal Flask backend with a clean, modular Python structure.
- Dark-themed, single-page frontend with no build step required.

## Project Structure

```
pdf_rag_app/
├── app.py                  # Flask routes only
├── config.py                # App-wide constants (models, chunk size, paths)
├── utils.py                  # Small shared helpers (e.g. allowed_file)
├── requirements.txt
├── rag/
│   ├── __init__.py           # Public API of the rag package
│   ├── extractor.py          # Text extraction and chunking
│   ├── embeddings.py          # Ollama embedding wrapper
│   ├── store.py                # ChromaDB indexing and retrieval
│   └── chat.py                  # Question answering and model listing
├── templates/
│   └── index.html               # Main UI page
└── static/
    ├── css/style.css              # Dark theme styling
    └── js/main.js                   # Upload, model select, and chat logic
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- Ollama models pulled locally, e.g.:
  ```
  ollama pull llama3.2
  ollama pull nomic-embed-text
  ```

## Installation

1. Clone or copy the project files into a folder.
2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Make sure the Ollama server is running:
   ```
   ollama serve
   ```

## Running the App

```
python app.py
```

The app will start on `http://127.0.0.1:5000`. Open this URL in your browser.

## Usage

1. Click **Choose file** and select a `.pdf`, `.txt`, or `.md` file.
2. Click **Build the book** to extract, chunk, embed, and index the document.
3. Once indexing completes, select a model from the dropdown (populated from your local Ollama models).
4. Type a question in the input box and press **Enter** or click **Send**.
5. The app retrieves the most relevant chunks from your document and asks the selected model to answer using only that context.

## Configuration

All key settings live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `CHAT_MODEL` | `llama3.2` | Default Ollama chat model |
| `EMBED_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `CHUNK_SIZE` | `512` | Characters per text chunk |
| `CHUNK_OVERLAP` | `100` | Overlap between consecutive chunks |
| `TOP_K` | `3` | Number of chunks retrieved per question |
| `UPLOAD_FOLDER` | `uploads` | Where uploaded files are stored |
| `ALLOWED_EXTENSIONS` | `.pdf, .txt, .md` | Accepted file types |
| `MAX_CONTENT_LENGTH` | `25 MB` | Max upload size |
| `CHROMA_PATH` | `./chroma_store` | ChromaDB persistence directory |

## How It Works

1. **Extraction** — `rag/extractor.py` pulls raw text out of the uploaded PDF, TXT, or Markdown file.
2. **Chunking** — the text is split into overlapping chunks to preserve context across boundaries.
3. **Embedding** — each chunk is converted into a vector using the `nomic-embed-text` model via Ollama.
4. **Storage** — vectors and chunk text are stored in a persistent ChromaDB collection (`rag/store.py`).
5. **Retrieval** — when a question is asked, it's embedded and the top-k most similar chunks are fetched.
6. **Answering** — the retrieved chunks are passed as context to the chosen chat model, which is instructed to answer only from that context or say "I don't know" (`rag/chat.py`).

## Notes

- Uploading a new file replaces the existing indexed collection (single-document mode).
- If no models are found or Ollama isn't running, the model dropdown and `/api/models` endpoint will show an error.
- This project is intended for local, single-user use and does not include authentication or multi-user support.

## License

MIT