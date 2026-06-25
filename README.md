# ServAI Monorepo

All-in-one AI operating system that replaces the executive team, marketing agency, call center, and operations department for home service businesses.

## 📁 Project Structure

- `backend/`: Python FastAPI application (Multi-agent orchestration, Business logic, Integrations).
- `frontend/`: Next.js dashboard and agent interface.
- `infra/`: Infrastructure as Code (Docker Compose, Kubernetes, Monitoring).
- `docs/`: Architecture diagrams and documentation.
- `scripts/`: Development and deployment utilities.

## 🚀 Quick Start (Local Development)

The fastest way to get started is using the provided setup script:

```bash
./scripts/setup-local.sh
```

Alternatively, you can use the `Makefile`:

```bash
make dev
```

### 🌍 Services
- **Unified Interface**: http://localhost:3000 (Proxies to Frontend & Backend)
- **Backend API**: http://localhost:3000/api
- **API Docs**: http://localhost:3000/docs
- **Postgres**: localhost:5432
- **Redis**: localhost:6379
- **Monitoring (Grafana)**: http://localhost:3001 (admin/admin)

## 🛠️ Commands (Makefile)

- `make dev`: Start development environment with hot-reload.
- `make build`: Build production Docker images.
- `make test`: Run all backend and frontend tests.
- `make deploy`: Deploy manifests to Kubernetes.
- `make clean`: Tear down containers and volumes.

## 🤝 Contributing

Please see [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for local setup, branching strategy, and coding standards.

## 🔒 Security & Multi-tenancy

- **RLS**: PostgreSQL Row-Level Security ensures data isolation between businesses.
- **Encryption**: Tenant-specific API keys are encrypted at rest.
- **Production Hardening**: Containers run as non-root users with restricted resource limits.

## 📈 Monitoring

The monitoring stack (Prometheus + Grafana) tracks:
- API response times and error rates.
- Agent task completion success.
- Resource utilization (CPU/Memory).
- Redis Pub/Sub health.
