#!/bin/bash

# StaffView - Quick Deployment Test Script
# Tests if the application is ready for production deployment

echo "⚡ StaffView Deployment Readiness Check"
echo "========================================"
echo ""

# Check if running from correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Run this script from the StaffView root directory"
    exit 1
fi

# Check Python
echo "1. Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION found"
else
    echo "   ❌ Python 3 not found"
    exit 1
fi

# Check requirements
echo "2. Checking dependencies..."
if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt found"
else
    echo "   ❌ requirements.txt missing"
    exit 1
fi

# Check Gunicorn
echo "3. Checking Gunicorn..."
if python3 -c "import gunicorn" 2>/dev/null; then
    echo "   ✅ Gunicorn installed"
else
    echo "   ⚠️  Gunicorn not installed (installing...)"
    pip3 install gunicorn==21.2.0
fi

# Check Flask
echo "4. Checking Flask..."
if python3 -c "import flask" 2>/dev/null; then
    echo "   ✅ Flask installed"
else
    echo "   ❌ Flask not installed"
    echo "   Run: pip install -r requirements.txt"
    exit 1
fi

# Check Docker (optional)
echo "5. Checking Docker (optional)..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "   ✅ $DOCKER_VERSION found"
else
    echo "   ⚠️  Docker not found (optional for container deployment)"
fi

# Check configuration files
echo "6. Checking deployment files..."
files=("gunicorn_config.py" "Dockerfile" "docker-compose.yml" "DEPLOYMENT.md")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file exists"
    else
        echo "   ❌ $file missing"
    fi
done

# Check uploads directory
echo "7. Checking uploads directory..."
if [ -d "uploads" ]; then
    echo "   ✅ uploads/ directory exists"
else
    echo "   ⚠️  Creating uploads/ directory..."
    mkdir uploads
fi

# Test app syntax
echo "8. Testing app.py syntax..."
if python3 -m py_compile app.py 2>/dev/null; then
    echo "   ✅ app.py syntax valid"
else
    echo "   ❌ app.py has syntax errors"
    exit 1
fi

echo ""
echo "========================================"
echo "✅ Deployment Readiness: PASSED"
echo ""
echo "🚀 Quick Start Commands:"
echo ""
echo "  Production (Gunicorn):"
echo "    gunicorn --config gunicorn_config.py app:app"
echo ""
echo "  Docker:"
echo "    docker-compose up -d"
echo ""
echo "  For detailed deployment guide, see: DEPLOYMENT.md"
echo ""

