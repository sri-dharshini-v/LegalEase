@echo off
title LegalEase AI Launcher
echo ========================================================
echo               LegalEase AI Starter Script                
echo ========================================================
echo.

if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment 'venv' not found.
    echo Please ensure venv is set up properly before running.
    pause
    exit /b 1
)

echo [1/2] Starting FastAPI Backend Server (Port 8000)...
start "LegalEase Backend" cmd /k "call venv\Scripts\activate.bat && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo [2/2] Starting Streamlit Frontend App (Port 8501)...
start "LegalEase Frontend" cmd /k "call venv\Scripts\activate.bat && streamlit run frontend/app.py --server.port 8501"

echo.
echo ========================================================
echo LegalEase AI is starting in separate windows!
echo - Backend API:  http://127.0.0.1:8000
echo - Frontend UI:  http://127.0.0.1:8501
echo ========================================================
echo.
