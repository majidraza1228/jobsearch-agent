#!/bin/bash

# Job Search AI Agent - Quick Start Script

echo "=================================="
echo "Job Search AI Agent - Quick Start"
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys"
    echo ""
    echo "cp .env.example .env"
    echo ""
    read -p "Press Enter to continue anyway or Ctrl+C to exit..."
fi

# Initialize database if it doesn't exist
if [ ! -f "jobs.db" ]; then
    echo "Initializing database..."
    python src/database/init_db.py
fi

echo ""
echo "=================================="
echo "Setup complete!"
echo "=================================="
echo ""
echo "Choose an option:"
echo "1. Run API Server (for n8n integration)"
echo "2. Search for jobs (CLI)"
echo "3. List jobs from database"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting API server..."
        echo "API will be available at http://localhost:5000"
        echo "Press Ctrl+C to stop"
        echo ""
        python src/api/server.py
        ;;
    2)
        echo ""
        read -p "Enter job keywords (e.g., 'Python Developer'): " keywords
        read -p "Enter location (e.g., 'Remote'): " location
        echo ""
        echo "Searching for jobs..."
        python -m src.main --search "$keywords" --location "$location" --limit 10
        ;;
    3)
        echo ""
        python -m src.main --list --limit 20
        ;;
    4)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
