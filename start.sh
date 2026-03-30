#!/bin/bash
# Production start script for Render

set -e

# Change to backend directory
cd backend

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database if needed
python -c "from app.database import init_db; init_db()"

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port $PORT
