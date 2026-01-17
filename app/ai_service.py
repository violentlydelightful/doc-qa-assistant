"""
AI service for answering questions about documents.
Supports multiple LLM providers with a pluggable architecture.
"""

import os
from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def answer_question(self, question: str, context: str) -> str:
        """Answer a question given document context."""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider."""

    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model

    def answer_question(self, question: str, context: str) -> str:
        if not self.api_key:
            return "Error: OpenAI API key not configured. Set OPENAI_API_KEY environment variable."

        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.api_key)

            system_prompt = """You are a helpful assistant that answers questions based on the provided document context.

Rules:
- Only answer based on the information in the context provided
- If the answer cannot be found in the context, say so clearly
- Be concise but thorough
- Quote relevant parts of the document when helpful"""

            user_prompt = f"""Document Context:
---
{context}
---

Question: {question}

Answer based only on the document context above:"""

            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error calling OpenAI API: {str(e)}"


class MockProvider(AIProvider):
    """Mock provider for testing without API keys."""

    def answer_question(self, question: str, context: str) -> str:
        # Simple keyword matching for demo purposes
        question_lower = question.lower()
        context_lower = context.lower()

        # Find sentences containing question keywords
        question_words = set(question_lower.split()) - {
            "what",
            "is",
            "the",
            "a",
            "an",
            "how",
            "why",
            "when",
            "where",
            "who",
            "does",
            "do",
            "can",
            "could",
            "would",
            "should",
        }

        sentences = context.replace("\n", " ").split(".")
        relevant = []

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in question_words):
                relevant.append(sentence.strip())

        if relevant:
            return f"Based on the document, here's what I found:\n\n{'. '.join(relevant[:3])}.\n\n(Note: This is a demo response. Configure OPENAI_API_KEY for full AI capabilities.)"
        else:
            return "I couldn't find specific information about that in the document. Try rephrasing your question or asking about different topics covered in the document.\n\n(Note: This is a demo response. Configure OPENAI_API_KEY for full AI capabilities.)"


def get_ai_provider(provider_name: str = "auto") -> AIProvider:
    """
    Get an AI provider instance.

    Args:
        provider_name: 'openai', 'mock', or 'auto' (uses OpenAI if key available)

    Returns:
        AIProvider instance
    """
    if provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "mock":
        return MockProvider()
    elif provider_name == "auto":
        if os.environ.get("OPENAI_API_KEY"):
            return OpenAIProvider()
        else:
            return MockProvider()
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
