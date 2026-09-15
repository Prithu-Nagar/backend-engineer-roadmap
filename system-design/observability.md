# Observability — Logs, Metrics, and Traces

Observability is the ability to understand what a production system is doing
from its external signals. The three core signals are logs, metrics, and
traces.

## Logs

Logs capture discrete events and useful diagnostic context.

Good production logs should include:

- Structured fields rather than only free-form messages
- Timestamp and severity
- Request or correlation ID
- Service and environment identity
- HTTP method, route, and status when relevant
- Exception context for failures

Avoid logging passwords, tokens, authorization headers, or complete sensitive
request bodies.

## Metrics

Metrics are numeric time-series measurements that make trends and alerts easy
to detect.

Common backend metrics include:

- Request rate
- Error rate
- Latency, especially p95/p99
- Active requests
- Dependency latency
- Database connection usage
- Queue depth
- Resource utilization

A useful alert normally combines a meaningful threshold with a sustained time
window rather than firing on one transient sample.

## Traces

Distributed traces connect work across services and dependencies.

```text
Client
  |
  v
API Gateway
  |
  +----> Task Service ----> PostgreSQL
  |
  +----> Redis
```

Each request can carry a trace context so a slow API request can be followed
into the service, database, cache, or downstream API that contributed to it.

## Health Checks

Liveness and readiness answer different questions:

- **Liveness:** should the orchestrator restart this process?
- **Readiness:** should this instance receive traffic right now?

A readiness check may validate required dependencies such as a database or
cache. A liveness check should stay lightweight and avoid failing merely
because an external dependency is temporarily unavailable.

## Operational Design

A production observability pipeline should support:

1. Structured application logs to stdout/stderr.
2. Metrics scraped or pushed to a monitoring system.
3. Trace context propagated across service boundaries.
4. Dashboards for traffic, latency, errors, and saturation.
5. Alerts tied to user-impacting symptoms and actionable thresholds.
6. Correlation between logs, metrics, and traces during incidents.
