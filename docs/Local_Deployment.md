# Local Deployment

## Step 1: Open the Project

Open the LegalEase project folder:

`LegalEaseAI`

## Step 2: Activate the Virtual Environment

Open Command Prompt in the project folder and run:

`venv\Scripts\activate.bat`

## Step 3: Start the FastAPI Backend

Run:

`python -m uvicorn backend.main:app --reload`

Backend URL:

`http://127.0.0.1:8000`

## Step 4: Start the Streamlit Frontend

Open another Command Prompt in the project folder and run:

`venv\Scripts\python.exe -m streamlit run frontend/app.py`

## Step 5: Verify the Application

Verify that:

- FastAPI backend is running.
- Streamlit frontend is accessible.
- Legal documents can be generated.
- Documents can be edited and previewed.
- TXT, DOCX, and PDF downloads work successfully.

The LegalEase application was successfully tested and verified for local deployment.