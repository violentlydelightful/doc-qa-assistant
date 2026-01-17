#!/usr/bin/env python3
"""
Document Q&A Assistant
Run this file to start the development server.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Document Q&A Assistant")
    print("=" * 50)
    print("\n  Starting server at: http://localhost:5001")
    print("\n  Note: Set OPENAI_API_KEY for full AI capabilities")
    print("        Without it, demo mode uses simple keyword matching")
    print("\n  Press Ctrl+C to stop\n")
    app.run(debug=True, port=5001)
