# CI/CD Pipeline Architecture

CI/CD creates an automated path from source-code change to a validated and
potentially deployable backend artifact.

---

## Pipeline Flow

```text
Developer
   |
   v
Pull Request / Push
   |
   v
+-------------------+
| Continuous        |
| Integration       |
| - lint            |
| - tests           |
| - build           |
+---------+---------+
          |
          v
   Versioned artifact
          |
          v
+-------------------+
| Deployment stage  |
| - migrate safely  |
| - deploy          |
| - health check    |
+---------+---------+
          |
          v
      Monitoring
```

---

## CI vs CD

| Concern | CI | CD |
|---|---|---|
| Trigger | Commit / pull request | Successful CI or release |
| Goal | Validate changes | Deliver validated changes |
| Typical checks | Lint, tests, build | Deploy, migrate, health check |
| Main risk | Broken code reaches main | Broken release reaches users |

---

## Pipeline Design Principles

- Keep fast feedback near the beginning of the pipeline.
- Fail fast on deterministic quality checks.
- Build the same artifact that will be deployed.
- Keep secrets in the CI/CD secret store, not source control.
- Make deployment steps observable and auditable.
- Treat database migrations as an explicit deployment concern.
- Add health checks before declaring a deployment successful.

---

## Repository Pipeline

This repository starts with CI rather than automatic production deployment.
The Day 43 workflow validates:

1. Python linting.
2. Automated tests.
3. Docker image construction.

Later production-engineering days can extend the same pipeline with deployment,
monitoring, security checks, and rollback strategies.
