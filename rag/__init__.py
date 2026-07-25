"""RAG (Retrieval-Augmented Generation) package.

Exposes the main functions used by the Flask app so callers can do:
    from rag import index_file, answer, has_document, list_chat_models
"""

from .extractor import extract_text, chunk_text
from .embeddings import embed
from .store import fresh_collection, index_file, retrieve, has_document
from .chat import answer, list_chat_models

__all__ = [
    "extract_text",
    "chunk_text",
    "embed",
    "fresh_collection",
    "index_file",
    "retrieve",
    "has_document",
    "answer",
    "list_chat_models",
]