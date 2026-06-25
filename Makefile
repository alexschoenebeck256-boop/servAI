.PHONY: dev build deploy test clean help

help:
	@echo "ServAI Monorepo Commands:"
	@echo "  make dev      - Start local development environment (with hot-reload)"
	@echo "  make build    - Build all docker images"
	@echo "  make test     - Run all tests (backend and frontend)"
	@echo "  make deploy   - Deploy to kubernetes"
	@echo "  make clean    - Stop and remove all containers"

dev:
	docker compose -f infra/docker-compose.yml -f infra/docker-compose.override.yml up --build

build:
	docker compose -f infra/docker-compose.yml build

test:
	@echo "Running backend tests..."
	cd backend && pytest
	@echo "Running frontend tests..."
	cd frontend && npm test

deploy:
	kubectl apply -f infra/k8s/

clean:
	docker compose -f infra/docker-compose.yml down -v
