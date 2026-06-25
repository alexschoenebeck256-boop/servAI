# Contributing to ServAI

Thank you for contributing to ServAI! This guide will help you get set up with our monorepo workflow.

## 📁 Repository Structure

- `backend/`: Python FastAPI code.
- `frontend/`: Next.js code.
- `infra/`: Docker, Kubernetes, and monitoring configurations.
- `docs/`: Architecture diagrams and documentation.
- `scripts/`: Development and deployment utilities.

## 🚀 Local Development Setup

1.  **Clone the Repository**:
    ```bash
    git clone <repo_url>
    cd servai
    ```
2.  **Initialize Environment**:
    ```bash
    ./scripts/setup-local.sh
    ```
    This script will create your `.env` file and start all services using `docker-compose`.

3.  **Manual Start**:
    Alternatively, use the Makefile:
    ```bash
    make dev
    ```

## 🛠️ Development Workflow

### Standard Commands
- `make dev`: Start dev environment with hot-reload.
- `make build`: Build docker images.
- `make test`: Run all tests.
- `make clean`: Clean up containers and volumes.

### Database Migrations (Alembic)
When changing the database schema:
1.  Enter the backend container: `docker-compose exec backend bash`
2.  Create migration: `alembic revision --autogenerate -m "description"`
3.  Apply migration: `alembic upgrade head`

## 🧪 Testing

- **Backend**: We use `pytest`. Run `cd backend && pytest`.
- **Frontend**: We use `jest`. Run `cd frontend && npm test`.

## 📜 Coding Standards

- **Python**: Follow PEP 8. We use `ruff` for linting.
- **TypeScript**: We use `eslint` and `prettier`.
- **Commits**: Follow Conventional Commits (e.g., `feat: add stripe integration`).

## 🚢 Pull Request Process

1.  Create a feature branch from `develop`.
2.  Ensure all tests pass and linting is clean.
3.  Open a PR against `develop`.
4.  Once approved and merged, it will be automatically deployed to staging.
