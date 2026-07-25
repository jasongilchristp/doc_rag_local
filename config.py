"""Application-wide configuration constants."""

CHAT_MODEL = "llama3.2"
EMBED_MODEL = "nomic-embed-text"
CHUNK_SIZE = 512
CHUNK_OVERLAP = 100
TOP_K = 3

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB

CHROMA_PATH = "./chroma_store"
COLLECTION_NAME = "documents"