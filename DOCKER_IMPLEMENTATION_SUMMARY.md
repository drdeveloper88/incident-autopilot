# 🔄 LLM Fallback & Docker Setup - Implementation Summary

**Date**: June 6, 2026  
**Version**: 2.0  
**Status**: ✅ Complete

## 📋 Overview

This implementation adds:
1. **Ollama Fallback Support**: Use local LLM (Ollama) if Groq API is unavailable
2. **Complete Docker Setup**: Containerized application with orchestration
3. **Production Readiness**: Docker Compose for dev/prod environments

---

## 🎯 What Was Implemented

### 1. LLM Fallback System

#### Modified Files:
- `backend/src/config/settings.py` - Added Ollama configuration
- `backend/src/workflows/sequential_issue_workflow.py` - Added fallback logic
- `backend/src/workflows/approval_based_workflow.py` - Added fallback logic
- `backend/.env` - Added Ollama settings

#### New Function: `_initialize_llm()`
```python
def _initialize_llm():
    """Initialize LLM with fallback support (Groq → Ollama)."""
    # Try Groq first
    if settings.groq_api_key:
        try:
            llm = ChatGroq(...)
            logger.info("✓ LLM initialized with Groq")
            return llm
        except:
            if not settings.use_ollama_fallback:
                raise
    
    # Fall back to Ollama
    if settings.ollama_enabled:
        try:
            llm = Ollama(...)
            logger.info("✓ LLM initialized with Ollama")
            return llm
        except:
            raise RuntimeError("No LLM provider available")
```

#### Configuration Options:
```env
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2
USE_OLLAMA_FALLBACK=true
```

---

### 2. Docker Infrastructure

#### New Files Created:

| File | Purpose |
|------|---------|
| `backend/Dockerfile` | Multi-stage build for FastAPI backend |
| `backend/.dockerignore` | Exclude unnecessary files from image |
| `frontend/Dockerfile` | Build and serve React frontend |
| `frontend/.dockerignore` | Exclude unnecessary files from image |
| `docker-compose.yml` | Development environment orchestration |
| `docker-compose.prod.yml` | Production environment setup |
| `DOCKER_SETUP.md` | Comprehensive Docker guide |
| `Makefile` | Convenient Docker commands |
| `docker-quick-start.sh` | Quick start script (Linux/Mac) |
| `docker-quick-start.ps1` | Quick start script (Windows) |

#### Docker Architecture:
```
Frontend (React)
├── Port: 3000
├── Base: node:18-alpine
└── Healthy

Backend (FastAPI)
├── Port: 8000
├── Base: python:3.11-slim
├── LLM: Groq → Ollama
└── Healthy

Ollama (LLM)
├── Port: 11434
├── Base: ollama/ollama:latest
├── Models: llama2, mistral, neural-chat
└── Healthy

Network: ticket-network (bridge)
```

#### Resource Limits (Production):
- Backend: 2 CPU, 4GB RAM (limits), 1 CPU, 2GB RAM (reserved)
- Frontend: 1 CPU, 1GB RAM (limits), 0.5 CPU, 512MB RAM (reserved)
- Ollama: 4 CPU, 8GB RAM (limits), 2 CPU, 4GB RAM (reserved)

---

### 3. Quick Start Scripts

#### Linux/Mac:
```bash
chmod +x docker-quick-start.sh
./docker-quick-start.sh
```

#### Windows (PowerShell):
```powershell
.\docker-quick-start.ps1
```

Both scripts:
- Check Docker prerequisites
- Validate configuration
- Offer dev/detached/prod modes
- Show service URLs
- Provide health checks

---

### 4. Makefile Commands

```bash
make help              # Show all commands
make build             # Build images
make up                # Start services
make down              # Stop services
make logs              # View all logs
make logs-backend      # View backend logs
make health            # Health check
make shell-backend     # SSH into backend
make pull-ollama-model # Pull model from Ollama
make stats             # Container stats
make prod-up           # Start production
```

---

## 🚀 Quick Start

### Development Mode
```bash
# Navigate to project
cd issue-resolution-agentic-platform

# Configure API key
echo "GROQ_API_KEY=your_key_here" >> backend/.env

# Start all services
docker-compose up

# Or use quick start
./docker-quick-start.sh  # Linux/Mac
.\docker-quick-start.ps1 # Windows

# Or use Makefile
make up
```

### Services Running
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs
- Ollama: http://localhost:11434

### Pull Ollama Model
```bash
# Option 1: Using Docker exec
docker exec ticket-resolution-ollama ollama pull llama2

# Option 2: Using Makefile
make pull-ollama-model

# Option 3: Direct command
docker-compose exec ollama ollama pull mistral
```

---

## 📊 Configuration Details

### Primary Provider (Groq)
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```
- Sign up: https://console.groq.com
- Get API key: https://console.groq.com/keys
- Models: llama-3.3-70b, mixtral-8x7b, gemma-7b

### Fallback Provider (Ollama)
```env
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2
USE_OLLAMA_FALLBACK=true
```
- Models: llama2, mistral, neural-chat, openchat
- Runs locally without API key
- Requires 6-12GB RAM

### Recommended Ollama Models
1. **llama2** (7B) - Default, good balance
2. **mistral** (7B) - Better quality, faster
3. **neural-chat** (7B) - Conversational optimized
4. **openchat** (7B) - Fast and competitive

---

## 🔍 Fallback Behavior

### How It Works:
1. **Start Backend**: `_initialize_llm()` is called
2. **Try Groq**: If API key exists, try ChatGroq
   - ✅ Success → Use Groq
   - ❌ Failure → Continue to step 3
3. **Fall Back to Ollama**: If Ollama enabled
   - ✅ Success → Use Ollama
   - ❌ Failure → Raise error
4. **Disable Fallback**: Set `USE_OLLAMA_FALLBACK=false` to error immediately

### Logs:
```
✓ LLM initialized with Groq: llama-3.3-70b-versatile
```
or
```
⚠ Failed to initialize Groq: Invalid API key
✓ LLM initialized with Ollama: llama2
```

---

## 🛠️ Production Deployment

### Using Production Compose
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Features:
- ✅ Auto-restart on failure
- ✅ Resource limits enforced
- ✅ Health checks every 30s
- ✅ JSON logging to files
- ✅ 3 max restart attempts
- ✅ Specific subnet (172.20.0.0/16)

### Scaling Backend
```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      replicas: 3  # Run 3 instances
```

### Push to Registry
```bash
docker tag issue-resolution-backend:latest myregistry/backend:latest
docker push myregistry/backend:latest
```

---

## 🧪 Testing

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Ollama health
curl http://localhost:11434/api/tags

# Frontend availability
curl http://localhost:3000
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama

# Last N lines
docker-compose logs --tail=50 backend
```

### Shell Access
```bash
# Backend (Python)
docker exec -it ticket-resolution-backend /bin/bash

# Frontend (Node)
docker exec -it ticket-resolution-frontend /bin/sh

# Ollama
docker exec -it ticket-resolution-ollama /bin/bash
```

---

## 📈 Performance Optimization

### For Ollama:
1. **Use GPU**: Install nvidia-docker, add to compose:
   ```yaml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: 1
             capabilities: [gpu]
   ```

2. **Larger Models**: Use 13B version
   ```bash
   docker exec ollama ollama pull llama2:13b
   ```

3. **Concurrent Requests**: Ollama handles via requests in parallel

### For Backend:
1. **Multiple Workers**: Modify Dockerfile CMD
   ```dockerfile
   CMD ["uvicorn", "...", "--workers", "4"]
   ```

2. **Connection Pooling**: Database connections are pooled

3. **Caching**: Responses can be cached per issue type

---

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Clean up
docker-compose down -v

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose up
```

### Ollama Out of Memory
```bash
# Check memory usage
docker stats ticket-resolution-ollama

# Use smaller model
docker exec ollama ollama pull llama2:7b
```

### Backend Can't Find Ollama
```bash
# Verify Ollama is running
docker-compose ps ollama

# Check network
docker network inspect ticket-resolution-agentic-platform_ticket-network

# Test connectivity
docker exec ticket-resolution-backend curl http://ollama:11434/api/tags
```

### Port Already in Use
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in docker-compose.yml
```

---

## 📚 Documentation

- **DOCKER_SETUP.md** - 400+ line comprehensive guide
- **Makefile** - Quick command reference
- **docker-compose.yml** - Development setup with comments
- **docker-compose.prod.yml** - Production setup with resources
- **.env.example** - Configuration template

---

## ✅ Verification Checklist

After setup:
- [ ] Docker and Docker Compose installed
- [ ] backend/.env configured with GROQ_API_KEY
- [ ] `docker-compose up` completes without errors
- [ ] Frontend loads at http://localhost:3000
- [ ] Backend responds at http://localhost:8000/health
- [ ] Ollama is running at http://localhost:11434
- [ ] Ollama model pulled: `docker exec ollama ollama pull llama2`
- [ ] Test ticket creation works
- [ ] Check logs: `docker-compose logs -f`

---

## 📝 Files Summary

| File | Type | Size | Purpose |
|------|------|------|---------|
| `backend/Dockerfile` | Docker | ~40 lines | Backend container build |
| `frontend/Dockerfile` | Docker | ~40 lines | Frontend container build |
| `docker-compose.yml` | YAML | ~120 lines | Dev environment |
| `docker-compose.prod.yml` | YAML | ~160 lines | Prod environment |
| `DOCKER_SETUP.md` | Markdown | ~400 lines | Complete guide |
| `Makefile` | Make | ~80 lines | Command shortcuts |
| `docker-quick-start.sh` | Bash | ~100 lines | Setup wizard (Linux/Mac) |
| `docker-quick-start.ps1` | PowerShell | ~130 lines | Setup wizard (Windows) |
| `backend/src/config/settings.py` | Python | Updated | Ollama config added |
| `backend/src/workflows/*.py` | Python | Updated | Fallback logic added |

---

## 🎓 Next Steps

1. **Start Services**
   ```bash
   docker-compose up -d
   ```

2. **Pull Ollama Model**
   ```bash
   docker exec ticket-resolution-ollama ollama pull llama2
   ```

3. **Test the System**
   - Visit http://localhost:3000
   - Create a test ticket
   - Verify AI analysis works

4. **Read Full Documentation**
   - See `DOCKER_SETUP.md` for advanced topics
   - Check `Makefile` for available commands

5. **Deploy to Production**
   - Use `docker-compose.prod.yml`
   - Configure CI/CD pipeline
   - Set resource limits
   - Enable monitoring

---

## 🔗 Resources

- **Docker Docs**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Ollama**: https://github.com/ollama/ollama
- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/

---

## 📞 Support

For issues:
1. Check `DOCKER_SETUP.md` Troubleshooting section
2. Review logs: `docker-compose logs`
3. Verify health: `docker-compose ps`
4. Check network: `docker network inspect [network-name]`

---

**Created**: June 6, 2026  
**Last Updated**: June 6, 2026  
**Status**: ✅ Complete & Ready for Use
