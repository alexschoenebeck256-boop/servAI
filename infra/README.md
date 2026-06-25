# ServAI Infrastructure & Deployment Guide

This directory contains the foundational infrastructure for the ServAI platform.

## Local Development (Docker Compose)

The easiest way to get the entire stack running locally is using Docker Compose.

### Prerequisites
- Docker and Docker Compose installed.

### Steps
1. Copy `.env.example` to `.env` and fill in your details:
   ```bash
   cp .env.example .env
   ```
2. Start the core services:
   ```bash
   docker-compose up --build
   ```
   This includes hot-reload for both Backend and Frontend via `docker-compose.override.yml`.

3. Start the monitoring stack (optional):
   ```bash
   docker-compose -f docker-compose.monitoring.yml up -d
   ```

### Core Services
- **Backend (FastAPI)**: `http://localhost:8000`
- **Frontend (Next.js)**: `http://localhost:3000`
- **PostgreSQL (pgvector)**: `localhost:5432`
- **Redis**: `localhost:6379`
- **Prometheus**: `http://localhost:9090`
- **Grafana**: `http://localhost:3001` (Default: admin/admin)

## Database Schema & Multi-tenancy

The database is initialized via `scripts/init-db.sql`, which includes:
- **Full Schema**: Businesses, Users, Customers, Leads, Jobs, Invoices, Agents, etc.
- **pgvector**: Support for vector embeddings in `knowledge_documents`.
- **RLS (Row-Level Security)**: Multi-tenant isolation at the database level. 
  - *Implementation*: Policies check `app.current_business_id`.

## CI/CD Pipeline

The CI/CD pipeline is configured via GitHub Actions in `.github/workflows/ci-cd.yml`.
- **Linting & Testing**: Runs on every push and PR to `main` and `develop`.
- **Building & Pushing**: Builds Docker images and pushes to DockerHub on every push to `main` or `develop`.
- **Deployment**: Deploys to Kubernetes on every push to `main`.

## Kubernetes Deployment

K8s manifests are located in the `k8s/` directory.

### To deploy manually:
1. Ensure you have `kubectl` configured with your cluster context.
2. Apply the configurations:
   ```bash
   kubectl apply -f k8s/
   ```

## Utilities
- `scripts/redis_health_check.py`: A Python utility for checking Redis Pub/Sub health.
