# ServAI Deployment Guide

This document outlines the procedures for deploying the ServAI platform to staging and production environments.

## 🏗️ Architecture Overview

The ServAI platform consists of:
- **Backend**: FastAPI Python application.
- **Frontend**: Next.js application.
- **Database**: PostgreSQL with `pgvector` extension.
- **Cache**: Redis.
- **Monitoring**: Prometheus and Grafana.

## 🚀 Staging Deployment (Docker Compose)

Staging is intended to mirror production as closely as possible.

### Prerequisites
- Docker and Docker Compose installed on the staging server.
- Access to the private container registry.

### Deployment Steps
1.  **Configure Environment**:
    ```bash
    cp infra/.env.production .env.staging
    # Edit .env.staging with staging-specific secrets
    ```
2.  **Pull and Start**:
    ```bash
    docker-compose -f infra/docker-compose.staging.yml pull
    docker-compose -f infra/docker-compose.staging.yml up -d
    ```
3.  **Verify Health**:
    ```bash
    ./scripts/verify-deployment.sh
    ```

## 🚢 Production Deployment (Kubernetes)

Production deployments are managed via Kubernetes manifests.

### Prerequisites
- `kubectl` configured with production cluster context.
- Secrets stored in a secure vault or Kubernetes Secrets.

### Deployment Steps
1.  **Apply Secrets**:
    Ensure `servai-secrets` is up to date in the target namespace.
2.  **Apply Manifests**:
    ```bash
    kubectl apply -f infra/k8s/
    ```
3.  **Monitor Rollout**:
    ```bash
    kubectl rollout status deployment/backend
    kubectl rollout status deployment/frontend
    ```

## 🔒 Secrets Management

Never commit real secrets to the repository.
- Use `.env.example` as a template.
- In CI/CD (GitHub Actions), use repository secrets.
- In Kubernetes, use `SealedSecrets` or an external provider like AWS Secrets Manager.

## 📈 Monitoring & Logs

- **Logs**: Access logs via `docker logs <container_id>` or `kubectl logs -f deployment/backend`.
- **Metrics**: Grafana dashboard is available at `https://monitor.servai.com`.
