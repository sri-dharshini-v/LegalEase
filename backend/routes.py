from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator
from backend.document_formatter import format_docx, format_pdf, format_html_preview, sanitize_text

router = APIRouter()
gemini_generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


class ExportRequest(BaseModel):
    document_text: str
    document_type: str


@router.post("/generate")
def generate_legal_document(request: DocumentRequest):
    try:
        raw_document = gemini_generator.generate_document(
            request.document_type,
            request.parties,
            request.terms,
            request.dates
        )
        sanitized_doc = sanitize_text(raw_document)
        return {
            "document": sanitized_doc
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/docx")
def export_docx(request: ExportRequest):
    try:
        docx_bytes = format_docx(request.document_text, request.document_type)
        filename = f"{request.document_type.replace(' ', '_').lower()}.docx"
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/export/pdf")
def export_pdf(request: ExportRequest):
    try:
        pdf_bytes = format_pdf(request.document_text, request.document_type)
        filename = f"{request.document_type.replace(' ', '_').lower()}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))