"""ChromaDB vector store operations: indexing, retrieval, and status checks."""

import chromadb
from config import CHROMA_PATH, COLLECTION_NAME, TOP_K
from .extractor import extract_text, chunk_text
from .embeddings import embed

_client = chromadb.PersistentClient(path=CHROMA_PATH)


def fresh_collection():
    """Delete any existing collection and create a new empty one."""
    try:
        _client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    return _client.get_or_create_collection(COLLECTION_NAME)


def index_file(filepath: str) -> int:
    """Extract, chunk, embed, and store a document's contents. Returns chunk count."""
    text = extract_text(filepath)
    chunks = chunk_text(text)
    if not chunks:
        raise ValueError(
            "No text found in the file. Please check the file format and content."
        )

    collection = fresh_collection()
    embeddings = [embed(chunk) for chunk in chunks]
    ids = [f"chunk-{i}" for i in range(len(chunks))]

    collection.add(ids=ids, documents=chunks, embeddings=embeddings)
    return len(chunks)


def retrieve(question: str, k: int = TOP_K) -> list[str]:
    """Return the top-k most relevant chunks for a question."""
    collection = _client.get_or_create_collection(COLLECTION_NAME)
    question_embedding = embed(question)
    results = collection.query(query_embeddings=[question_embedding], n_results=k)
    return results["documents"][0] if results["documents"] else []


def has_document() -> bool:
    """Check whether any document has been indexed yet."""
    try:
        collection = _client.get_or_create_collection(COLLECTION_NAME)
        return collection.count() > 0
    except Exception:
        return False