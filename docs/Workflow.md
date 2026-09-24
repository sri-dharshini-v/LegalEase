# Workflow

1. User enters the required legal document details in the Streamlit frontend.
2. Streamlit sends the document request to the FastAPI backend.
3. FastAPI receives the request through the `/generate` API route.
4. The backend sends the document details to the Gemini AI model.
5. Gemini generates the legal document content.
6. The generated document is returned to the Streamlit frontend.
7. The user can edit and preview the generated document.
8. The document can be exported as TXT, DOCX, or PDF.