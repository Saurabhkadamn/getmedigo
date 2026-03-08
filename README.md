# GetMedigo - Microservice Foundation

This repository includes a production-oriented microservice starter architecture for the website-first phase.

## Services
- **api-gateway**: public entrypoint and service routing.
- **auth-service**: authentication endpoints (**currently stubbed**).
- **user-service**: profile endpoints.
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

## Tests
```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## CI
GitHub Actions workflow: `.github/workflows/ci.yml`

## Architecture docs
- `docs/architecture/microservices.md`
- `docs/roadmap/next-steps.md`
- `docs/roadmap/release-readiness.md`

## Is this production-ready right now?
Not yet. It is a strong scaffold, but see `docs/roadmap/release-readiness.md` for launch blockers and minimum go-live gates.
