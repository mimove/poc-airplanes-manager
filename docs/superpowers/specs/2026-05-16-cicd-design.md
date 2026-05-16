# CI/CD Design — poc-airplanes-manager

**Date:** 2026-05-16
**Status:** Approved

## Goal

Automate quality gates on every PR (lint, tests, build) and publish Docker images to Docker Hub on every merge to `main`. EC2/Kubernetes deployment is handled manually for now and is out of scope.

## Repository

`github.com/mimove/poc-airplanes-manager`

## Workflow Files

Two separate GitHub Actions workflow files:

| File | Trigger | Purpose |
|------|---------|---------|
| `.github/workflows/ci.yml` | push to any branch, PR to main | Lint, test, build verification |
| `.github/workflows/cd.yml` | push to main only | Build + push Docker images to Docker Hub |

Branch protection on `main` must require CI to pass before merge so CD only runs on verified code.

## CI Workflow (`.github/workflows/ci.yml`)

**Triggers:**
- `push` — all branches
- `pull_request` — targeting `main`

**Jobs:**

### `backend`

Runner: `ubuntu-latest`

Steps:
1. Checkout repo
2. Install uv (official `astral-sh/setup-uv` action)
3. `uv sync --frozen` — installs all deps including dev group
4. `uv run ruff check app/ tests/` — lint
5. `uv run ruff format --check app/ tests/` — format check
6. `uv run pytest tests/unit/ -v` — unit tests (no external deps)
7. `uv run pytest tests/integration/ -v` — integration tests (testcontainers spins up PostgreSQL via Docker, which is available on `ubuntu-latest` runners)

### `frontend`

Runner: `ubuntu-latest`

Steps:
1. Checkout repo
2. Setup Node 20 (`actions/setup-node@v4`)
3. `npm ci` — reproducible install from `package-lock.json`
4. `npm run test` — Vitest unit tests
5. `npm run build` — Vite production build (catches type errors / import issues)

## CD Workflow (`.github/workflows/cd.yml`)

**Trigger:** `push` to `main` only

**Assumption:** Branch protection ensures CI must pass before merge; CD does not re-run tests.

**Jobs:**

### `build-push`

Runner: `ubuntu-latest`

Steps:
1. Checkout repo
2. Setup Docker Buildx (`docker/setup-buildx-action@v3`)
3. Login to Docker Hub (`docker/login-action@v3`) using secrets
4. Build and push backend image: `mimove/poc-airplanes-manager-backend:latest`
5. Build and push frontend image: `mimove/poc-airplanes-manager-frontend:latest`

Both images use the existing `Dockerfile` in their respective directories. Images are built with `--push` flag so they are pushed directly without a separate push step.

## Docker Hub Images

| Image | Tag | Source |
|-------|-----|--------|
| `mimove/poc-airplanes-manager-backend` | `latest` | `./backend/Dockerfile` |
| `mimove/poc-airplanes-manager-frontend` | `latest` | `./frontend/Dockerfile` |

## GitHub Secrets Required

Set in **Settings → Secrets and variables → Actions**:

| Secret | Value |
|--------|-------|
| `DOCKERHUB_USERNAME` | `mimove` |
| `DOCKERHUB_TOKEN` | Docker Hub access token (not password) — create at hub.docker.com → Account Settings → Security |

## Out of Scope

- EC2 deployment automation (handled manually, Kubernetes/microk8s planned)
- Image tagging with git SHA (can be added later for rollback support)
- Slack/email notifications on failure
- Docker image scanning (Trivy, etc.)
