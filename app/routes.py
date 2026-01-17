import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app, session
from werkzeug.utils import secure_filename
from app.document_processor import extract_text, chunk_text, get_document_stats
from app.ai_service import get_ai_provider

main = Blueprint("main", __name__)

# In-memory storage for uploaded documents (use database in production)
documents = {}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in current_app.config["ALLOWED_EXTENSIONS"]
    )


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Supported: txt, pdf, docx, md"}), 400

    # Generate unique ID for this document
    doc_id = str(uuid.uuid4())[:8]
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{doc_id}_{filename}")

    file.save(filepath)

    # Extract text from document
    text = extract_text(filepath)
    stats = get_document_stats(text)

    # Store document info
    documents[doc_id] = {
        "id": doc_id,
        "filename": filename,
        "filepath": filepath,
        "text": text,
        "chunks": chunk_text(text),
        "stats": stats,
    }

    # Clean up the file after extraction (optional - comment out to keep files)
    # os.remove(filepath)

    return jsonify(
        {
            "success": True,
            "doc_id": doc_id,
            "filename": filename,
            "stats": stats,
        }
    )


@main.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    doc_id = data.get("doc_id")
    question = data.get("question")

    if not doc_id or not question:
        return jsonify({"error": "Missing doc_id or question"}), 400

    if doc_id not in documents:
        return jsonify({"error": "Document not found. Please upload a document first."}), 404

    doc = documents[doc_id]

    # For simplicity, use full text if it's small enough, otherwise use chunks
    # In production, you'd use embeddings and semantic search
    context = doc["text"]
    if len(context) > 8000:
        # Use first few chunks as context (simplified approach)
        context = "\n\n".join(doc["chunks"][:4])

    # Get AI response
    provider = get_ai_provider("auto")
    answer = provider.answer_question(question, context)

    return jsonify(
        {
            "success": True,
            "question": question,
            "answer": answer,
            "doc_id": doc_id,
        }
    )


@main.route("/documents")
def list_documents():
    doc_list = [
        {
            "id": doc["id"],
            "filename": doc["filename"],
            "stats": doc["stats"],
        }
        for doc in documents.values()
    ]
    return jsonify({"documents": doc_list})


@main.route("/document/<doc_id>")
def get_document(doc_id):
    if doc_id not in documents:
        return jsonify({"error": "Document not found"}), 404

    doc = documents[doc_id]
    return jsonify(
        {
            "id": doc["id"],
            "filename": doc["filename"],
            "stats": doc["stats"],
            "preview": doc["text"][:500] + "..." if len(doc["text"]) > 500 else doc["text"],
        }
    )
