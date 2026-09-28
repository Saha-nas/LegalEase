from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import generate_legal_document

router = APIRouter()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        document = generate_legal_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates,
        )
    except RuntimeError as exc:
        if "gemini models are temporarily unavailable" in str(exc).lower():
            raise HTTPException(
                status_code=503,
                detail="Gemini is busy right now. Please wait a minute and try again.",
            ) from exc
        raise

    return {
        "document_type": request.document_type,
        "document": document,
    }