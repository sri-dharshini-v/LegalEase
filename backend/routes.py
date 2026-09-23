from fastapi import APIRouter
from pydantic import BaseModel

from backend.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate_document(request: DocumentRequest):

    document = generator.generate_document(
        request.document_type,
        request.parties,
        request.terms,
        request.dates
    )

    return {
        "document": document
    }