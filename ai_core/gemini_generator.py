import os
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

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text