# Production-Readiness Checklist

Use this checklist to review a backend project before presenting it as production-oriented portfolio work. Mark an item complete only when the repository or deployment provides evidence for it.

## API and Application Behavior

- [ ] Request payloads and query parameters are validated.
- [ ] Responses use consistent status codes and error formats.
- [ ] Authentication and resource-level authorization are enforced where required.
- [ ] Pagination and bounded request sizes prevent unbounded work.
- [ ] Timeouts and safe retry behavior are defined for external dependencies.
- [ ] Idempotency is considered for retryable write operations.

## Data and Transactions

- [ ] Database constraints protect critical invariants.
- [ ] Transaction boundaries cover multi-step business operations.
- [ ] Migrations are version-controlled and reviewed.
- [ ] Indexes are justified by representative query plans.
- [ ] Connection pools and query timeouts are configured.
- [ ] Backup and recovery expectations are documented.

## Testing and Code Quality

- [ ] Unit tests cover business logic and edge cases.
- [ ] Integration tests cover database and API behavior.
- [ ] Authorization failures and invalid inputs are tested.
- [ ] Concurrency-sensitive operations have appropriate tests.
- [ ] Linters, formatters, and tests run consistently.
- [ ] Dependencies are pinned or constrained intentionally.

## Security and Configuration

- [ ] Secrets are not committed or logged.
- [ ] Configuration is separated by environment.
- [ ] Least privilege is applied to application and database access.
- [ ] Inputs and outputs are handled safely.
- [ ] Dependencies and base images are reviewed for known vulnerabilities.
- [ ] Sensitive information is excluded from public errors and telemetry.

## Containers and Deployment

- [ ] The image builds reproducibly and excludes unnecessary files.
- [ ] The service runs as a non-root user where practical.
- [ ] Health checks reflect readiness and process health appropriately.
- [ ] Graceful shutdown and connection draining are considered.
- [ ] Migrations are compatible with the deployment sequence.
- [ ] Rollback or mitigation steps are documented.

## Observability and Operations

- [ ] Logs include useful context without secrets or unnecessary personal data.
- [ ] Errors, latency, throughput, and resource saturation can be monitored.
- [ ] Correlation IDs help trace a request across relevant components.
- [ ] Alerts have actionable thresholds and an owner.
- [ ] Common failure modes have troubleshooting steps.
- [ ] Service dependencies and recovery assumptions are documented.

## Portfolio Evidence

- [ ] README explains the problem, architecture, setup, and configuration.
- [ ] API examples and test instructions are reproducible.
- [ ] Architecture decisions and trade-offs are documented.
- [ ] Known limitations are stated honestly.
- [ ] Resume claims map to implementation and test evidence.
- [ ] No real secrets, private data, or unrelated local artifacts are included.

## Review Outcome

Record remaining gaps, their impact, and the next action. This checklist is a review aid, not a claim that the application is certified or production-safe merely because every box is checked.
