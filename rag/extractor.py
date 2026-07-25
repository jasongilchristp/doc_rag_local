"""Text extraction and chunking utilities."""

from PyPDF2 import PdfReader
from config import CHUNK_SIZE, CHUNK_OVERLAP


def extract_text(filepath: str) -> str:
    """Extract raw text from a PDF, TXT, or Markdown file."""
    if filepath.lower().endswith(".pdf"):
        reader = PdfReader(filepath)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text into overlapping chunks for embedding."""
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    step = max(size - overlap, 1)
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks