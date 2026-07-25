"""Embedding helper wrapping the Ollama embeddings API."""

import ollama
from config import EMBED_MODEL


def embed(text: str):
    """Return the embedding vector for a piece of text."""
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]