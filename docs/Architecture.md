# LegalEase – Application Architecture

## Activity 1.2: Define the Architecture of the Application

### 1. Frontend

Streamlit is used as the frontend for user interaction.

Responsibilities:
- Accept document input from the user
- Display generated document content
- Allow document editing
- Provide download options

### 2. Backend

FastAPI is used as the backend.

Responsibilities:
- Receive API requests
- Process user input
- Route requests to the Gemini AI integration
- Return generated document content

### 3. AI Core

Gemini integration is used for AI-powered document generation.

The GeminiDocumentGenerator forms a structured prompt and sends it to Gemini using generate_content.

### 4. Formatting Modules

The application supports document formatting and export in:

- DOCX
- PDF
- TXT

### 5. Application Flow

User
↓
Streamlit Frontend
↓
FastAPI Backend
↓
Gemini AI Core
↓
Generated Legal Document
↓
Streamlit Preview
↓
Edit / Download as TXT, DOCX or PDF
