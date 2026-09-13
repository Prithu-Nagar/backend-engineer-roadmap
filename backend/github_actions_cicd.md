# GitHub Actions CI/CD

GitHub Actions can automate repository validation and connect successful CI runs
to later delivery stages.

---

## CI Workflow

A typical backend workflow should validate every pull request and push:

```text
Push / Pull Request
        |
        v
  Checkout source
        |
        v
 Install dependencies
        |
   +----+----+
   |         |
   v         v
  Lint      Test + Coverage
   |         |
   +----+----+
        |
        v
   Build artifact/image
        |
        v
    CI result
```

The repository workflow in `.github/workflows/ci.yml` provides this quality gate.

---

## GitHub Actions Building Blocks

| Component | Purpose |
|---|---|
| Workflow | Defines automation triggered by repository events |
| Job | Groups steps that run on a runner |
| Step | Performs one command or reusable action |
| Runner | Execution environment for the job |
| Artifact | Build output that can be passed to later jobs |
| Secret | Protected value used without committing credentials |

---

## CI/CD Separation

CI answers:

> Is this change safe to merge?

CD answers:

> Can this validated artifact be delivered safely?

A production pipeline should promote the same validated artifact instead of
rebuilding different source code at each deployment stage.

---

## Coverage

Coverage measures which executable paths are exercised by automated tests. It is
a signal of test completeness, not proof that the application is correct.

Useful checks include:

- Run coverage on every pull request.
- Publish a coverage report as a CI artifact when useful.
- Track meaningful changes in coverage over time.
- Avoid treating a high percentage as a substitute for good test cases.

---

## Production Guardrails

Before extending CI into deployment, add:

- Protected environments.
- Explicit deployment approvals where required.
- Secret management through GitHub environments or an equivalent secret store.
- Database migration checks.
- Post-deployment health checks.
- Rollback or roll-forward procedures.
