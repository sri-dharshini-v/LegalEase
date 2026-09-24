#!/bin/bash
echo "========================================================"
echo "              LegalEase AI Starter Script               "
echo "========================================================"
echo ""

if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "[1/2] Starting FastAPI Backend Server (Port 8000)..."
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

sleep 3

echo "[2/2] Starting Streamlit Frontend App (Port 8501)..."
streamlit run frontend/app.py --server.port 8501

kill $BACKEND_PID
