"""Chat / question-answering logic built on top of retrieval."""

import ollama
from config import CHAT_MODEL
from .store import retrieve


def answer(question: str, model: str = CHAT_MODEL) -> str:
    """Answer a question using retrieved context and the chat model."""
    chunks = retrieve(question)
    if not chunks:
        return "No document loaded yet. Please upload a document first."

    context = "\n\n".join(chunks)

    prompt = (
        "Use only the following context to answer the question. "
        "If the answer is not contained within the context, say 'I don't know'.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
    )

    response = ollama.chat(
        model=model or CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def list_chat_models() -> list[str]:
    """List available Ollama chat models (excluding embedding models)."""
    data = ollama.list()
    models = data.get("models", []) if isinstance(data, dict) else data.models

    names = []
    for m in models:
        name = (
            (m.get("model") or m.get("name"))
            if isinstance(m, dict)
            else (getattr(m, "model", None) or getattr(m, "name", None))
        )
        if name and "embed" not in name.lower():
            names.append(name)
    return sorted(names)