# Issue Resolution Agentic Platform - Docker Quick Start (PowerShell)
# Usage: .\docker-quick-start.ps1

Write-Host "╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  Issue Resolution Agentic Platform - Docker Quick Start        ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check prerequisites
Write-Host "📋 Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

if (-not (Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose is not installed. Please install Docker Compose." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Docker and Docker Compose are installed" -ForegroundColor Green
Write-Host ""

# Check if .env exists
Write-Host "⚙️  Checking configuration..." -ForegroundColor Yellow

if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  backend\.env not found. Creating from example..." -ForegroundColor Yellow
    if (Test-Path "backend\.env.example") {
        Copy-Item "backend\.env.example" "backend\.env"
        Write-Host "📝 Please edit backend\.env and add your GROQ_API_KEY" -ForegroundColor Yellow
        Write-Host "   You can get it from: https://console.groq.com" -ForegroundColor Yellow
        exit 1
    } else {
        Write-Host "❌ backend\.env.example not found" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✓ Configuration found" -ForegroundColor Green
Write-Host ""

# Ask which mode to run
Write-Host "🚀 Starting services..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Select start mode:" -ForegroundColor Cyan
Write-Host "  1) Development (with logs)"
Write-Host "  2) Detached (background)"
Write-Host "  3) Production"
Write-Host ""

$choice = Read-Host "Enter choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "📊 Starting in development mode..." -ForegroundColor Yellow
        docker-compose build
        docker-compose up
    }
    "2" {
        Write-Host "🎯 Starting in detached mode..." -ForegroundColor Yellow
        docker-compose build
        docker-compose up -d
        
        Write-Host ""
        Write-Host "✓ Services are running!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Access applications:" -ForegroundColor Cyan
        Write-Host "  • Frontend:  http://localhost:3000"
        Write-Host "  • Backend:   http://localhost:8000"
        Write-Host "  • API Docs:  http://localhost:8000/docs"
        Write-Host "  • Ollama:    http://localhost:11434"
        Write-Host ""
        Write-Host "📊 View logs:" -ForegroundColor Cyan
        Write-Host "  • All:       docker-compose logs -f"
        Write-Host "  • Backend:   docker-compose logs -f backend"
        Write-Host "  • Frontend:  docker-compose logs -f frontend"
        Write-Host ""
        Write-Host "🛑 Stop services:" -ForegroundColor Cyan
        Write-Host "  • docker-compose down"
        Write-Host ""
    }
    "3" {
        Write-Host "🏭 Starting in production mode..." -ForegroundColor Yellow
        docker-compose -f docker-compose.prod.yml build
        docker-compose -f docker-compose.prod.yml up -d
        
        Write-Host ""
        Write-Host "✓ Production services are running!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📍 Access applications:" -ForegroundColor Cyan
        Write-Host "  • Frontend:  http://localhost:3000"
        Write-Host "  • Backend:   http://localhost:8000"
        Write-Host ""
        
        Start-Sleep -Seconds 5
        Write-Host "🏥 Health check:" -ForegroundColor Yellow
        
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "  ✓ Backend is healthy" -ForegroundColor Green
            } else {
                Write-Host "  ⚠️  Backend is starting..." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "  ⚠️  Backend is starting..." -ForegroundColor Yellow
        }
        
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:3000" -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200) {
                Write-Host "  ✓ Frontend is healthy" -ForegroundColor Green
            } else {
                Write-Host "  ⚠️  Frontend is starting..." -ForegroundColor Yellow
            }
        } catch {
            Write-Host "  ⚠️  Frontend is starting..." -ForegroundColor Yellow
        }
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "💡 Next steps:" -ForegroundColor Cyan
Write-Host "  1. Visit http://localhost:3000"
Write-Host "  2. Create a new ticket"
Write-Host "  3. Watch the AI analysis"
Write-Host ""
Write-Host "📚 For more info, see DOCKER_SETUP.md" -ForegroundColor Cyan
