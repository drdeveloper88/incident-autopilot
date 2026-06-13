# 🐳 Docker Quick Reference

## Start & Stop

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart
```

## Viewing Services

```bash
# List running services
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f ollama

# Last 50 lines
docker-compose logs --tail=50

# Logs since time
docker-compose logs --since 5m
```

## Building

```bash
# Build all images
docker-compose build

# Build specific service
docker-compose build backend

# Build without cache
docker-compose build --no-cache

# Build for production
docker-compose -f docker-compose.prod.yml build
```

## Execution

```bash
# Run one-off command
docker-compose exec backend python -m pip list

# Open shell in container
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh
docker-compose exec ollama /bin/bash

# Run tests
docker-compose exec backend python -m pytest
```

## Health & Stats

```bash
# Health check
curl http://localhost:8000/health
curl http://localhost:11434/api/tags
curl http://localhost:3000

# Container stats
docker stats

# Container resource usage
docker-compose stats
```

## Ollama Models

```bash
# Pull a model
docker exec ollama ollama pull llama2
docker exec ollama ollama pull mistral

# List models
docker exec ollama curl http://localhost:11434/api/tags

# Remove model
docker exec ollama ollama rm llama2
```

## Cleanup

```bash
# Remove stopped containers
docker-compose down

# Remove all (containers + volumes)
docker-compose down -v

# Clean up dangling images
docker image prune

# Full cleanup
docker system prune -a
```

## Using Makefile

```bash
make help           # Show all commands
make build          # Build images
make up             # Start services
make down           # Stop services
make logs           # View logs
make logs-backend   # Backend logs only
make health         # Health check
make shell-backend  # SSH to backend
make stats          # Resource usage
make prod-up        # Start production
```

## Using Quick Start Scripts

### Linux/Mac
```bash
chmod +x docker-quick-start.sh
./docker-quick-start.sh
```

### Windows (PowerShell)
```powershell
.\docker-quick-start.ps1
```

## Configuration

### Set Environment Variables
```bash
# Edit backend/.env
export GROQ_API_KEY=your_key_here
export OLLAMA_MODEL=mistral

# Or use .env file
cp backend/.env.example backend/.env
# Edit backend/.env
```

### Check Environment in Container
```bash
docker-compose exec backend env
```

## Production Commands

```bash
# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Stop production services
docker-compose -f docker-compose.prod.yml down

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Production health check
docker-compose -f docker-compose.prod.yml ps
```

## Docker Network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect ticket-resolution-agentic-platform_ticket-network

# Test connectivity between containers
docker exec backend curl http://ollama:11434/api/tags
```

## Useful Flags

| Flag | Purpose |
|------|---------|
| `-d` | Detached mode (background) |
| `-f` | Follow logs |
| `--tail=N` | Last N lines |
| `--build` | Build before starting |
| `-v` | Remove volumes |
| `--no-cache` | Rebuild without cache |
| `--scale N` | Scale service to N replicas |

## URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React app |
| Backend | http://localhost:8000 | FastAPI |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Ollama | http://localhost:11434 | LLM service |

## Common Issues

```bash
# Service won't start
docker-compose down -v
docker-compose build --no-cache
docker-compose up

# Can't connect to service
docker-compose ps              # Check status
docker-compose logs            # Check logs
docker network inspect [name]  # Check network

# Out of memory
docker stats                    # Check usage
docker system prune -a         # Free space
```

## Example Workflow

```bash
# 1. Start development
docker-compose up -d

# 2. Check status
docker-compose ps

# 3. View logs
docker-compose logs -f backend

# 4. Pull Ollama model
docker exec ollama ollama pull mistral

# 5. Test health
curl http://localhost:8000/health

# 6. Access frontend
open http://localhost:3000

# 7. Stop when done
docker-compose down
```

---

For more details, see `DOCKER_SETUP.md`
