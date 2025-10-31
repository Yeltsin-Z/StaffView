#!/bin/bash

# Start script for Artifact Comparison Tool

echo "🚀 Starting Artifact Comparison Tool..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies if Flask is not installed
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
fi

# Start the server
echo ""
echo "🌐 Starting server on http://localhost:5001"
echo "📊 Press Ctrl+C to stop the server"
echo ""

python app.py

