"""Flask application entry point: routes only, logic lives in rag/ and utils.py."""

import os
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename

from config import CHAT_MODEL, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from utils import allowed_file
from rag import index_file, answer, has_document, list_chat_models

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html", has_document=has_document())


@app.route("/api/models")
def api_models():
    try:
        models = list_chat_models()
        return jsonify({"models": models, "default": CHAT_MODEL})
    except Exception:
        return jsonify({
            "models": [],
            "error": "Could not reach Ollama API. Please ensure the Ollama server is running."
        }), 500


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No file selected."}), 400

    file = request.files["file"]
    if not allowed_file(file.filename): # type: ignore
        return jsonify({"error": "Invalid file type. Only PDF, Text or Markdown files are allowed."}), 400

    filename = secure_filename(file.filename) # type: ignore
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    try:
        chunk_count = index_file(filepath)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"Error occurred while processing the file: {str(e)}"}), 500

    return jsonify({"filename": filename, "chunks": chunk_count})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    model = (data.get("model") or "").strip() or CHAT_MODEL
    if not question:
        return jsonify({"error": "Ask a question first."}), 400

    try:
        reply = answer(question, model)
    except Exception as e:
        return jsonify({"error": f"Error occurred while generating the answer: {str(e)}"}), 500

    return jsonify({"answer": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)