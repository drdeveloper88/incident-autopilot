.PHONY: help build up down logs clean restart ps health

help:
	@echo "Issue Resolution Agentic Platform - Docker Commands"
	@echo ""
	@echo "Usage: make [command]"
	@echo ""
	@echo "Available commands:"
	@echo "  help              - Show this help message"
	@echo "  build             - Build all Docker images"
	@echo "  up                - Start all services"
	@echo "  down              - Stop all services"
	@echo "  ps                - Show running services"
	@echo "  logs              - Show logs from all services"
	@echo "  logs-backend      - Show backend logs"
	@echo "  logs-frontend     - Show frontend logs"
	@echo "  logs-ollama       - Show ollama logs"
	@echo "  clean             - Remove all containers and volumes"
	@echo "  restart           - Restart all services"
	@echo "  health            - Check health of all services"
	@echo "  shell-backend     - Open shell in backend container"
	@echo "  shell-frontend    - Open shell in frontend container"
	@echo "  shell-ollama      - Open shell in ollama container"
	@echo "  pull-ollama-model - Pull a model from Ollama"
	@echo "  stats             - Show container resource usage"
	@echo "  test              - Run tests"
	@echo "  prod-up           - Start production services"
	@echo "  prod-down         - Stop production services"
	@echo ""

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✓ Services started"
	@make health

down:
	docker-compose down
	@echo "✓ Services stopped"

ps:
	docker-compose ps

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-ollama:
	docker-compose logs -f ollama

clean:
	docker-compose down -v --remove-orphans
	@echo "✓ All containers and volumes removed"

restart:
	docker-compose restart
	@echo "✓ Services restarted"

health:
	@echo "Checking service health..."
	@curl -s http://localhost:8000/health | python -m json.tool || echo "Backend: FAILED"
	@curl -s http://localhost:3000 > /dev/null && echo "Frontend: OK" || echo "Frontend: FAILED"
	@curl -s http://localhost:11434/api/tags > /dev/null && echo "Ollama: OK" || echo "Ollama: FAILED"

shell-backend:
	docker exec -it ticket-resolution-backend /bin/bash

shell-frontend:
	docker exec -it ticket-resolution-frontend /bin/sh

shell-ollama:
	docker exec -it ticket-resolution-ollama /bin/bash

pull-ollama-model:
	@read -p "Enter model name (e.g., llama2, mistral): " model; \
	docker exec ticket-resolution-ollama ollama pull $$model

stats:
	docker stats

test:
	docker-compose exec backend python -m pytest

prod-up:
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✓ Production services started"
	@sleep 5
	@make health

prod-down:
	docker-compose -f docker-compose.prod.yml down
	@echo "✓ Production services stopped"

.DEFAULT_GOAL := help
