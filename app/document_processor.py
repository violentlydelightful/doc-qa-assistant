"""
Document processing utilities for extracting text from various file formats.
"""

import os
from pathlib import Path


def extract_text_from_txt(filepath: str) -> str:
    """Extract text from a plain text file."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_from_pdf(filepath: str) -> str:
    """Extract text from a PDF file."""
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(filepath)
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        return "\n\n".join(text_parts)
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def extract_text_from_docx(filepath: str) -> str:
    """Extract text from a Word document."""
    try:
        from docx import Document

        doc = Document(filepath)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"


def extract_text_from_markdown(filepath: str) -> str:
    """Extract text from a Markdown file (same as txt)."""
    return extract_text_from_txt(filepath)


def extract_text(filepath: str) -> str:
    """
    Extract text from a document based on its file extension.

    Supports: .txt, .pdf, .docx, .md
    """
    ext = Path(filepath).suffix.lower()

    extractors = {
        ".txt": extract_text_from_txt,
        ".pdf": extract_text_from_pdf,
        ".docx": extract_text_from_docx,
        ".md": extract_text_from_markdown,
    }

    extractor = extractors.get(ext)
    if extractor:
        return extractor(filepath)
    else:
        return f"Unsupported file format: {ext}"


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list[str]:
    """
    Split text into overlapping chunks for processing.

    Args:
        text: The text to chunk
        chunk_size: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence or paragraph boundary
        if end < len(text):
            # Look for paragraph break
            newline_pos = text.rfind("\n\n", start, end)
            if newline_pos > start + chunk_size // 2:
                end = newline_pos + 2
            else:
                # Look for sentence break
                for sep in [". ", "! ", "? ", "\n"]:
                    pos = text.rfind(sep, start, end)
                    if pos > start + chunk_size // 2:
                        end = pos + len(sep)
                        break

        chunks.append(text[start:end].strip())
        start = end - overlap

    return chunks


def get_document_stats(text: str) -> dict:
    """Get basic statistics about a document."""
    words = text.split()
    paragraphs = [p for p in text.split("\n\n") if p.strip()]

    return {
        "characters": len(text),
        "words": len(words),
        "paragraphs": len(paragraphs),
        "estimated_tokens": len(text) // 4,  # Rough estimate
    }
