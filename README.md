# LegalEase: AI-Powered Legal Document Generator

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/sri-dharshini-v/LegalEase)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/AI-Google%20Gemini%201.5%20Pro-8E44AD.svg)](https://deepmind.google/technologies/gemini/)

**LegalEase** leverages state-of-the-art Generative AI (Google Gemini 1.5 Pro) to simplify the creation of legal documents by providing customizable, accurate, and editable templates for a wide range of use cases (Employment Contracts, Lease Agreements, NDAs, Service Contracts, etc.).

---

## 🚀 Features

- **AI-Powered Generation**: Generates comprehensive, legally sound documents tailored to involved parties, effective dates, and specific terms/conditions.
- **FastAPI Backend**: Robust API with dedicated endpoints for generation (`/generate`) and multi-format document exporting (`/export/docx`, `/export/pdf`).
- **Interactive Streamlit UI**: User-friendly web application with input forms, styled dark-themed HTML preview, and inline text editor.
- **Multi-Format Export Options**:
  - **📄 .TXT**: Plain text export.
  - **📝 .DOCX**: Formatted Microsoft Word document with company logo, Times New Roman typography, auto-generated Terms table, and footer.
  - **📕 .PDF**: Branded PDF document with logo headers, bold section titles, bullet-point formatting, and page footers.
- **Input Sanitization**: Clean handling of typographic quotes, Unicode characters, and currency symbols.

---

## 🏗️ Architecture

```
User Input (Streamlit Frontend)
       │
       ▼
POST /generate (FastAPI Backend)
       │
       ▼
ai_core/gemini_generator.py (Gemini 1.5 Pro Model)
       │
       ▼
Generated Legal Content
       │
       ▼
Streamlit Preview Card & Inline Editor
       │
       ▼
Export as .TXT / .DOCX / .PDF
```

---

## 📂 Project Structure

```
LegalEaseAI/
├── ai_core/
│   ├── __init__.py
│   └── gemini_generator.py     # Gemini 1.5 Pro AI core generator
├── backend/
│   ├── document_formatter.py   # DOCX, PDF, and HTML preview formatting
│   ├── main.py                 # FastAPI application initialization
│   └── routes.py               # API routes (/generate, /export/docx, /export/pdf)
├── docs/
│   ├── Architecture.md         # System architecture specification
│   ├── Conclusion.md           # Project conclusion and summary
│   ├── FastAPI_Backend.md      # Backend API documentation
│   ├── Local_Deployment.md     # Deployment guide
│   ├── Prerequisites.md       # Environment requirements
│   ├── Task_1_Model_Selection.md # Gemini AI model selection analysis
│   └── Workflow.md             # End-to-end data flow documentation
├── frontend/
│   ├── app.py                  # Streamlit frontend user interface
│   └── Image/
│       ├── Logo.png            # Branded application logo
│       └── inverseLogo.png     # Dark mode logo variant
├── .env                        # Gemini API Key configuration
├── config.py                   # Global configuration and path settings
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── run.bat                     # Windows batch launcher
└── run.sh                      # Linux/macOS shell launcher
```

---

## 🛠️ Prerequisites & Setup

### Requirements
- **Python 3.10+**
- **Google Gemini API Key**

### 1. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/sri-dharshini-v/LegalEase.git
cd LegalEase

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate.bat
# Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-pro
```

---

## 💻 Running the Application

### Option A: Launcher Script (Recommended)

**Windows:**
```cmd
run.bat
```

**Linux / macOS:**
```bash
chmod +x run.sh
./run.sh
```

### Option B: Manual Startup

**1. Launch FastAPI Backend Server (Port 8000):**
```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```
- API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`

**2. Launch Streamlit Frontend Application (Port 8501):**
```bash
streamlit run frontend/app.py --server.port 8501
```
- Web Application Interface: `http://127.0.0.1:8501`

---

## 📧 Contact & Repository

- **GitHub Repository**: [sri-dharshini-v/LegalEase](https://github.com/sri-dharshini-v/LegalEase)
- **Contact Email**: [s86015049@gmail.com](mailto:s86015049@gmail.com)
