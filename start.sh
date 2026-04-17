#!/bin/bash
echo "Starting Emora AI Prototype..."

echo "1. Installing backend dependencies..."
python3 -m pip install -r requirements.txt

echo "2. Starting the Python NLP Backend (server.py) on port 8000..."
python3 server.py &
BACKEND_PID=$!

echo "3. Starting the Frontend server on port 5500..."
python3 -m http.server 5500 &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are running! The chatbot humanoid responses will now work."
echo "   - Frontend: http://localhost:5500"
echo "   - Backend:  http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers."

trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT TERM
wait
