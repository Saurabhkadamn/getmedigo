# What Next: Execution Plan (Post-Scaffold)

This plan turns the current scaffold into a production-capable platform in incremental milestones.

## Milestone 1 (Week 1): Core hygiene and contracts
- Add OpenAPI contract export for each service and publish in CI artifacts.
- Enforce semantic API versioning (`/api/v1`) standards across services.
- Add request validation/error format standard (`code`, `message`, `request_id`).
- Add DB migration tooling (Alembic) for service-owned schemas.

## Milestone 2 (Week 2-3): Real data and auth
- Implement real auth flow (password hashing + JWT issuance/rotation).
- Introduce PostgreSQL persistence for users and auth sessions.
- Add Redis-backed rate limiting in gateway.
- Add integration tests for login/profile/content across gateway.

## Milestone 3 (Week 4): Async and reliability
- Introduce message broker (RabbitMQ/Kafka/SQS) for async events.
- Add worker service for emails/notifications.
- Add retries with exponential backoff for gateway downstream calls.
- Implement readiness checks for DB/cache dependencies.

## Milestone 4 (Week 5): Security and observability
- Add structured JSON logging with correlation IDs.
- Add Prometheus metrics and Grafana dashboards.
- Add Sentry (or equivalent) for error tracking.
- Add secrets management and environment hardening.

## Milestone 5 (Week 6): Deployment and scale readiness
- Add Kubernetes manifests or Helm charts.
- Configure horizontal pod autoscaling rules by CPU and latency.
- Run load testing targetting peak assumptions for 50k users.
- Define SLOs and alert thresholds before go-live.

## Immediate owner checklist
1. Finalize `Product.md` with exact user journeys and role model.
2. Prioritize first domain service after content/auth/user (likely booking).
3. Decide cloud target (AWS/GCP/Azure) for production IaC direction.
