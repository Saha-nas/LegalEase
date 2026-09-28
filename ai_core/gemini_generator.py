import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def generate_legal_document(document_type, parties, terms, dates):
    prompt = f"""
You are a legal document drafting assistant.

Generate a professional {document_type}.

Parties:
{parties}

Terms and Conditions:
{terms}

Dates:
{dates}

Create a clear and well-structured document.
Use appropriate headings and clauses.
Do not invent important facts that were not provided.
"""

    # A temporary overload of one Gemini model should not make the whole app
    # fail. Try the current model first, then supported alternatives.
    models = (
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.1-flash-lite",
    )
    last_error = None

    for index, model in enumerate(models):
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            if not response.text:
                raise RuntimeError(f"Gemini returned an empty response using {model}.")
            return response.text
        except Exception as exc:
            last_error = exc
            status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
            # Only switch models for temporary overloads. Other errors (for
            # example an invalid API key) should be reported immediately.
            if status_code != 503:
                raise
            if index < len(models) - 1:
                time.sleep(index + 1)

    raise RuntimeError(
        "Gemini models are temporarily unavailable. Please try again in a few minutes."
    ) from last_error
