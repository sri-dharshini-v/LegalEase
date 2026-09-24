# FastAPI Backend

LegalEase uses FastAPI to provide the backend API for legal document generation.

## Backend Components

- `backend/main.py` initializes the FastAPI application.
- `backend/routes.py` contains the API routes.
- `backend/gemini_generator.py` handles Gemini AI document generation.
- `POST /generate` receives the document details and returns the generated legal document.

## Verification

The FastAPI backend was tested successfully using the Swagger UI at:

`http://127.0.0.1:8000/docs`

The `/generate` endpoint returned **200 OK** and generated the requested legal document successfully.