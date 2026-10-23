# Day 84 — Deployment and Operations Review

## Deployment objectives

A deployment plan should balance release speed with safety, observability, and recoverability.

- **Reproducibility:** deploy an immutable image built from a known commit.
- **Safety:** run tests, dependency/image scans, and configuration validation before promotion.
- **Availability:** choose a rollout strategy that matches the service's tolerance for interruption.
- **Recoverability:** define rollback triggers, owners, and the last known-good artifact.
- **Observability:** compare error rate, latency, saturation, and business signals before and after release.

## Delivery pipeline

1. Validate formatting, lint, type checks, and unit tests.
2. Run integration/contract tests against controlled dependencies.
3. Build a versioned container image and attach commit/build metadata.
4. Scan dependencies and the image; fail on policy-defined critical findings.
5. Publish the immutable artifact to a registry.
6. Deploy to a test/staging environment and run smoke checks.
7. Promote gradually, monitoring health and service-level indicators.
8. Record the release and preserve a tested rollback path.

## Rollout strategies

| Strategy | Benefit | Risk / trade-off |
|---|---|---|
| Rolling | Gradually replaces instances | Mixed versions may coexist |
| Blue/green | Fast traffic switch and rollback | Requires capacity for both environments |
| Canary | Limits initial blast radius | Needs reliable metrics and traffic controls |

## Operational readiness checklist

- [ ] Readiness and liveness checks have distinct purposes.
- [ ] Shutdown drains requests and closes connections gracefully.
- [ ] Secrets are injected at runtime and never baked into images.
- [ ] CPU, memory, replica, and connection-pool limits are explicit.
- [ ] Migrations are compatible with rolling deployment order.
- [ ] Alerts use actionable thresholds and identify an owner.
- [ ] Rollback triggers and procedures have been rehearsed.
- [ ] Backups and restore procedures have been tested.
- [ ] Runbooks cover common failures, escalation, and communication.

## Incident exercise

A new release doubles p95 latency and increases HTTP 5xx errors.

1. Confirm the change window and compare release markers on dashboards.
2. Check error rate, p95/p99 latency, saturation, and dependency health.
3. Stop promotion; roll back if agreed thresholds are crossed.
4. Preserve logs, traces, metrics, and the relevant deployment metadata.
5. Verify recovery after rollback and create a follow-up action with an owner.

Do not treat a successful container start as proof that the service is healthy. Validate the user-facing request path and its dependencies.
