# Day 84 — Capstone Implementation Sprint 2

## Sprint objective

Continue the Day 83 service-boundary work by preparing the capstone for reproducible packaging, deployment, and operational review. Preserve existing behavior and avoid claiming production readiness without evidence.

## Sprint scope

1. Confirm the application entry point, runtime version, and dependency installation process.
2. Externalize environment-specific configuration and validate required settings at startup.
3. Define a repeatable container build and a non-root runtime where practical.
4. Add or verify CI gates for tests, linting, and dependency/image scanning.
5. Document health checks, database migration order, rollout, rollback, and smoke-test steps.
6. Validate database connection limits, least-privilege access, backup/restore expectations, and migration safety.

## Implementation plan

- Use the existing application and project configuration; do not replace established modules with generic examples.
- Pin or constrain dependencies and build from a clean environment.
- Keep secrets out of source control and container layers.
- Build an immutable image tagged with a version or commit identifier.
- Run automated tests before deployment and smoke-test the deployed request path.
- Record any infrastructure-specific steps that cannot be executed locally.

## Acceptance criteria

- [ ] A clean environment can install dependencies using documented steps.
- [ ] Missing required configuration fails clearly without exposing secrets.
- [ ] Tests and lint checks run in CI before the artifact is promoted.
- [ ] Container image and runtime configuration are documented.
- [ ] Readiness checks verify the service can accept traffic.
- [ ] Database migrations and connection limits are reviewed.
- [ ] Rollback and post-deployment smoke checks are documented.
- [ ] No production-readiness claim is made without verified tests and deployment evidence.

## Next sprint

Review performance and caching, identify measured bottlenecks, and add Redis/cache behavior only where justified by the capstone's actual access patterns.
