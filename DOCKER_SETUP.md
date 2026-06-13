# 🐳 Docker Setup Guide

Complete Docker setup for the Issue Resolution Agentic Platform with Groq (primary) and Ollama (fallback) LLM support.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start](#quick-start)
4. [Configuration](#configuration)
5. [Building Images](#building-images)
6. [Running Services](#running-services)
7. [Managing Models](#managing-models)
8. [Troubleshooting](#troubleshooting)
9. [Production Deployment](#production-deployment)

## 🏗️ Architecture Overview

The application uses a multi-container Docker setup:

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Network                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Frontend   │  │   Backend    │  │    Ollama    │  │
│  │  (Port 3000) │  │  (Port 8000) │  │ (Port 11434) │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│                         │                      │         │
│                    Primary LLM              Fallback    │
│                    (Groq API)              (Local LLM)  │
└─────────────────────────────────────────────────────────┘
```

### Services

- **Frontend**: React application (Node.js 18-alpine)
- **Backend**: FastAPI application (Python 3.11-slim)
- **Ollama**: Local LLM service for fallback (ollama/ollama:latest)

## 📦 Prerequisites

### Required
- Docker Desktop (20.10+) or Docker Engine
- Docker Compose (2.0+)
- 8GB RAM minimum (12GB+ recommended)
- 20GB free disk space

### Optional
- Groq API Key (for primary LLM provider)
  - Sign up at: https://console.groq.com
  - Create an API key in settings
- GPU support (for faster Ollama inference)

## 🚀 Quick Start

### 1. Clone and Navigate
```bash
cd issue-resolution-agentic-platform
```

### 2. Configure Environment
```bash
# Copy example environment file if needed
cp backend/.env.example backend/.env 2>/dev/null || true

# Edit backend/.env with your Groq API key
# GROQ_API_KEY=your_groq_api_key_here
```

### 3. Start All Services
```bash
# Build and start all services
docker-compose up --build

# Or in detached mode
docker-compose up -d --build
```

### 4. Verify Services
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Test backend health
curl http://localhost:8000/health

# Test frontend
open http://localhost:3000
```

### 5. Stop Services
```bash
docker-compose down

# Remove volumes as well
docker-compose down -v
```

## ⚙️ Configuration

### Environment Variables

Create or edit `backend/.env`:

```env
# Primary LLM Provider (Groq)
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Fallback LLM Provider (Ollama)
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2
USE_OLLAMA_FALLBACK=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Logging
LOG_LEVEL=INFO
```

### Frontend Configuration

The frontend automatically connects to the backend at `http://localhost:8000`.

To change this in production, set:
```bash
REACT_APP_API_URL=https://your-backend-url.com
```

## 🔨 Building Images

### Build All Services
```bash
docker-compose build
```

### Build Specific Service
```bash
# Backend only
docker-compose build backend

# Frontend only
docker-compose build frontend
```

### Build for Production
```bash
# Build with optimization
docker-compose build --no-cache

# Push to registry
docker tag issue-resolution-backend:latest your-registry/backend:latest
docker push your-registry/backend:latest
```

## ▶️ Running Services

### Development Mode
```bash
# Start with live logs
docker-compose up

# Or in background
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama
```

### Production Mode
```bash
# Start in detached mode with auto-restart
docker-compose up -d

# Verify health
docker-compose ps

# View only errors
docker-compose logs --tail=50 --follow --level=ERROR
```

### Scale Services
```bash
# Run multiple backend instances (requires load balancer)
docker-compose up -d --scale backend=3
```

## 🤖 Managing Models

### Ollama Models

#### Pull a Model
```bash
# Pull llama2 (latest)
docker exec ticket-resolution-ollama ollama pull llama2

# Pull specific version
docker exec ticket-resolution-ollama ollama pull llama2:13b

# List available models
# - llama2 (7B, default)
# - llama2:13b (13B)
# - mistral (7B)
# - neural-chat (7B)
# - openchat (7B)
```

#### Recommended Models

For **Production**:
```bash
# Pull Mistral (better performance/quality)
docker exec ticket-resolution-ollama ollama pull mistral

# Update .env
OLLAMA_MODEL=mistral
```

For **GPU Inference** (faster):
```bash
# Pull with GPU support (check your VRAM)
docker exec ticket-resolution-ollama ollama pull mistral:7b
docker exec ticket-resolution-ollama ollama pull neural-chat
```

#### List Downloaded Models
```bash
curl http://localhost:11434/api/tags
```

#### Delete a Model
```bash
docker exec ticket-resolution-ollama ollama rm llama2
```

### Monitor Model Performance
```bash
# Check Ollama resource usage
docker stats ticket-resolution-ollama

# View detailed logs
docker logs -f ticket-resolution-ollama
```

## 🔧 Troubleshooting

### Services Won't Start

**Problem**: `docker-compose up` fails
```bash
# Solution 1: Check Docker daemon
docker ps

# Solution 2: Clean up and rebuild
docker-compose down -v
docker-compose up --build --no-cache

# Solution 3: Check logs
docker-compose logs
```

### Backend Can't Connect to Ollama

**Problem**: "Failed to initialize Ollama fallback"
```bash
# Solution 1: Verify Ollama is running
docker-compose ps ollama

# Solution 2: Check Ollama health
docker exec ticket-resolution-ollama curl http://localhost:11434/api/tags

# Solution 3: Check network
docker network inspect ticket-resolution-agentic-platform_ticket-network
```

### Frontend Can't Reach Backend

**Problem**: "Failed to create ticket: API error"
```bash
# Solution 1: Check backend is healthy
curl http://localhost:8000/health

# Solution 2: Check CORS is enabled
# Backend already has CORS enabled in src/api/main.py

# Solution 3: Check network connectivity
docker exec ticket-resolution-frontend curl http://backend:8000/health
```

### Ollama Out of Memory

**Problem**: Ollama crashes with OOM
```bash
# Solution 1: Reduce model size
docker exec ticket-resolution-ollama ollama pull llama2:7b

# Solution 2: Increase Docker memory limit
# Edit docker-compose.yml, add to ollama service:
# deploy:
#   resources:
#     limits:
#       memory: 8G

# Solution 3: Monitor memory usage
docker stats ticket-resolution-ollama
```

### Port Conflicts

**Problem**: "Address already in use"
```bash
# Solution: Change ports in docker-compose.yml
# Or kill existing processes:
lsof -i :8000   # Find backend
lsof -i :3000   # Find frontend
lsof -i :11434  # Find Ollama

# Kill process
kill -9 <PID>
```

## 📊 Production Deployment

### Docker Image Registry

#### Push to Docker Hub
```bash
# Login
docker login

# Tag images
docker tag issue-resolution-backend:latest your-username/backend:latest
docker tag issue-resolution-frontend:latest your-username/frontend:latest

# Push
docker push your-username/backend:latest
docker push your-username/frontend:latest
```

#### Push to Private Registry
```bash
# Tag for your registry
docker tag issue-resolution-backend:latest registry.example.com/backend:latest

# Push
docker push registry.example.com/backend:latest
```

### Security Best Practices

1. **Use Secrets Management**
   ```bash
   # Create secret for API key
   docker secret create groq_api_key -
   ```

2. **Enable TLS**
   ```nginx
   # Add reverse proxy (Nginx/Traefik) in front
   # docker-compose.prod.yml
   ```

3. **Health Checks**
   - Already configured in docker-compose.yml
   - Monitors: `GET /health` endpoints

4. **Resource Limits**
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

### Scaling

#### Horizontal Scaling
```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
```

#### Load Balancing
```bash
# Add Nginx load balancer
# Or use Docker Swarm/Kubernetes
docker swarm init
docker stack deploy -c docker-compose.yml app
```

### Monitoring

#### Collect Metrics
```bash
# Enable Prometheus metrics
# Add to backend environment:
METRICS_ENABLED=true

# Access metrics
curl http://localhost:8000/metrics
```

#### View Container Stats
```bash
# Real-time stats
docker stats

# Historical logs
docker logs --since 1h ticket-resolution-backend
```

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
# .github/workflows/docker.yml
name: Build and Push Docker Images

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker/setup-buildx-action@v1
      - uses: docker/login-action@v1
        with:
          registry: docker.io
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v2
        with:
          context: ./backend
          push: true
          tags: username/backend:latest
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Docker Best Practices](https://reactjs.org/docs/getting-started.html)

## 💡 Tips & Tricks

### Quick Commands
```bash
# Restart all services
docker-compose restart

# Remove everything
docker-compose down -v --remove-orphans

# Update single service
docker-compose up -d --no-deps --build backend

# Shell into container
docker exec -it ticket-resolution-backend /bin/bash
docker exec -it ticket-resolution-frontend /bin/sh

# Run one-off command
docker-compose exec backend python -m pip list
```

### Development Workflow
```bash
# Edit code locally
# Changes auto-reload in development

# Test changes
curl http://localhost:8000/health

# View real-time logs
docker-compose logs -f --tail=50

# Rebuild if needed
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Performance Optimization

1. **Backend**: Use uvicorn workers
   - Modify Dockerfile CMD: `uvicorn ... --workers 4`

2. **Frontend**: Enable gzip compression
   - Already configured in build

3. **Ollama**: Use GPU acceleration
   - Install nvidia-docker
   - Add GPU device to docker-compose.yml

## 📝 License

Same as main project

---

**Last Updated**: June 2026
**Version**: 1.0
