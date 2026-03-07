# GetMedigo Microservice Architecture (Website-first)

> **Note:** `Product.md` is currently empty, so this design uses pragmatic assumptions for a healthcare-focused startup website and can be refined once product requirements are finalized.

## Goals
- Production-ready baseline for website launch.
- Horizontally scalable to support at least **50,000 registered users**.
- Clear service boundaries to reduce coupling and support independent deployments.
- Security and observability from day 1.

## Assumed Scale Envelope
- 50,000 registered users.
- 8,000-12,000 monthly active users in early growth.
- 500-1,500 peak concurrent sessions.
- 150-300 API requests/sec at peak traffic windows.

## Service Topology

```text
Client (Web/Mobile)
  -> API Gateway
      -> Auth Service
      -> User Service
      -> Content Service
      -> Future: Booking Service, Payments Service, Notifications Service

Shared Infrastructure:
- PostgreSQL (primary relational data)
- Redis (cache, rate limits, sessions, idempotency keys)
- Message Broker (future async workloads)
- Object Storage (media and documents)
```

## Initial Services

### 1) API Gateway
**Responsibility**
- Entry-point for all client traffic.
- Route requests to internal services.
- Enforce request correlation IDs.
- Handle edge rate-limits and coarse auth checks.

### 2) Auth Service
**Responsibility**
- Signup/login/token issuance.
- Password reset and session invalidation.
- Future support for OAuth/social login and MFA.

### 3) User Service
**Responsibility**
- User profile CRUD.
- Preferences and account metadata.
- Future role/permission enrichment.

### 4) Content Service
**Responsibility**
- Public website content API (pages/articles/FAQs metadata).
- Health/status endpoints.
- Future CMS integration.

## Data Design Principles
- Each service owns its own schema/tables (logical ownership even if initially one PostgreSQL cluster).
- Cross-service interactions via HTTP APIs (synchronous) and events (asynchronous in future).
- No direct table access across service boundaries.

## Reliability and Scalability
- Run all services as containers.
- Start with stateless services and horizontal autoscaling.
- Multi-instance deployment for gateway and critical services.
- Health/readiness endpoints for orchestration.
- Add message queues for high-latency workflows (email, notifications, webhooks).

## Security Baseline
- TLS termination at ingress/load balancer.
- JWT-based auth for internal API calls where needed.
- Secret management through environment variables + secret store (not committed to repo).
- Rate limiting at gateway.
- Audit logs for auth-sensitive operations.

## Observability Baseline
- Structured JSON logs with `request_id` correlation.
- Prometheus metrics endpoints for each service (next step).
- Error tracking integration (e.g., Sentry).
- Dashboard: p95 latency, 5xx rate, service saturation.

## Deployment Plan
- Local: `docker-compose`.
- Production target: Kubernetes or managed container runtime.
- CI/CD: build once, deploy immutable images.
- Rollout strategy: rolling or blue/green with automatic rollback gates.

## Next Steps
1. Finalize product requirements in `Product.md`.
2. Add booking and notification services based on actual user journeys.
3. Introduce async event bus and worker services.
4. Add contract tests between gateway and downstream services.
