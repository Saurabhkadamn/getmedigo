# GetMedigo - Microservice Foundation

This repository includes a production-oriented microservice starter architecture for the website-first phase.

## Services
- **api-gateway**: public entrypoint and service routing.
- **auth-service**: authentication endpoints (stubbed for now).
- **user-service**: profile endpoints (stubbed for now).
- **content-service**: website content endpoints.

## Infra (local)
- PostgreSQL 16
- Redis 7
- Docker Compose orchestration

## Run locally
```bash
docker compose up --build
```

## Quick checks
```bash
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'content-type: application/json' \
  -d '{"email":"demo@getmedigo.com","password":"secret"}'
curl http://localhost:8000/api/v1/users/user-123
curl http://localhost:8000/api/v1/content/home
```

## Test route contracts
```bash
python -m unittest tests/test_route_contracts.py
```

## CI
GitHub Actions workflow: `.github/workflows/ci.yml`

## Architecture doc
See `docs/architecture/microservices.md` for scale, security, reliability, and next-step details.

## Delivery roadmap
See `docs/roadmap/next-steps.md` for the next implementation milestones.
