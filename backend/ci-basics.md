# CI Basics

Continuous Integration (CI) automatically validates changes before they are merged.
A backend CI pipeline should provide fast feedback while protecting the repository
from broken tests, formatting issues, and invalid builds.

---

## Core CI Stages

| Stage | Purpose |
|---|---|
| Checkout | Fetch the exact commit being validated |
| Setup | Install a supported Python runtime |
| Dependencies | Install application and test dependencies |
| Lint | Detect style and static-quality problems |
| Test | Run automated unit/integration tests |
| Build | Verify the application/container can be built |

---

## Why CI Matters

CI turns quality checks into a repeatable repository rule instead of relying only
on a developer's local environment.

Good CI should be:

- Reproducible.
- Fast enough for normal pull requests.
- Deterministic.
- Easy to diagnose when a check fails.
- Independent of developer-specific machine configuration.

---

## Linting

Linting catches common problems before tests or deployment. The repository uses
Ruff in CI as a lightweight Python linting check.

```text
Pull Request
     |
     v
  Install
     |
     +----> Ruff lint
     |
     +----> Pytest
     |
     +----> Docker build
     |
     v
  CI result
```

---

## Tests

Tests should run against the same dependency set expected by the project. CI
should fail when a test fails rather than allowing later deployment steps to hide
the failure.

---

## Build Validation

A successful container build verifies that the Dockerfile, dependency installation,
source layout, and image build context remain compatible.

The workflow in `.github/workflows/ci.yml` implements these checks for this repository.
