#!/bin/bash

# Issue Resolution Agentic Platform - Docker Quick Start
# Usage: ./docker-quick-start.sh

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Issue Resolution Agentic Platform - Docker Quick Start        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"
echo ""

# Check if .env exists
echo "⚙️  Checking configuration..."

if [ ! -f "backend/.env" ]; then
    echo "⚠️  backend/.env not found. Creating from example..."
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo "📝 Please edit backend/.env and add your GROQ_API_KEY"
        echo "   You can get it from: https://console.groq.com"
        exit 1
    else
        echo "❌ backend/.env.example not found"
        exit 1
    fi
fi

echo "✓ Configuration found"
echo ""

# Ask which mode to run
echo "🚀 Starting services..."
echo ""
echo "Select start mode:"
echo "  1) Development (with logs)"
echo "  2) Detached (background)"
echo "  3) Production"
echo ""

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "📊 Starting in development mode..."
        docker-compose build
        docker-compose up
        ;;
    2)
        echo "🎯 Starting in detached mode..."
        docker-compose build
        docker-compose up -d
        
        echo ""
        echo "✓ Services are running!"
        echo ""
        echo "📍 Access applications:"
        echo "  • Frontend:  http://localhost:3000"
        echo "  • Backend:   http://localhost:8000"
        echo "  • API Docs:  http://localhost:8000/docs"
        echo "  • Ollama:    http://localhost:11434"
        echo ""
        echo "📊 View logs:"
        echo "  • All:       docker-compose logs -f"
        echo "  • Backend:   docker-compose logs -f backend"
        echo "  • Frontend:  docker-compose logs -f frontend"
        echo ""
        echo "🛑 Stop services:"
        echo "  • docker-compose down"
        echo ""
        ;;
    3)
        echo "🏭 Starting in production mode..."
        docker-compose -f docker-compose.prod.yml build
        docker-compose -f docker-compose.prod.yml up -d
        
        echo ""
        echo "✓ Production services are running!"
        echo ""
        echo "📍 Access applications:"
        echo "  • Frontend:  http://localhost:3000"
        echo "  • Backend:   http://localhost:8000"
        echo ""
        
        sleep 5
        echo "🏥 Health check:"
        
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            echo "  ✓ Backend is healthy"
        else
            echo "  ⚠️  Backend is starting..."
        fi
        
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo "  ✓ Frontend is healthy"
        else
            echo "  ⚠️  Frontend is starting..."
        fi
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "💡 Next steps:"
echo "  1. Visit http://localhost:3000"
echo "  2. Create a new ticket"
echo "  3. Watch the AI analysis"
echo ""
echo "📚 For more info, see DOCKER_SETUP.md"
