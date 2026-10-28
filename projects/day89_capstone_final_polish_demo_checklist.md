# Day 89 — Capstone Final Polish and Demo Checklist

## Objective

Prepare the capstone for a reliable portfolio walkthrough. This is a final polish pass: document what exists, validate the setup and tests, fix high-impact issues, and make the demo repeatable. Do not claim features or results that have not been verified.

## README acceptance checklist

- [ ] Project purpose, intended users, and key features are clear.
- [ ] Technology stack matches the implementation.
- [ ] Prerequisites and setup steps work in a clean environment.
- [ ] Environment variables are listed with safe example values; no secrets are committed.
- [ ] API endpoint table matches the actual routes, methods, auth, payloads, and status codes.
- [ ] Data model, relationships, constraints, and important indexes are documented.
- [ ] Architecture diagram reflects the code that exists.
- [ ] Test, lint, and formatting commands are copy-pasteable and their results are current.
- [ ] Logging, health checks, troubleshooting, limitations, and deferred work are documented.
- [ ] No placeholder claims, dead links, credentials, or production identifiers remain.

## Final validation sequence

1. Start from a clean checkout or a fresh virtual environment.
2. Follow the README setup steps exactly.
3. Run the documented tests and quality checks; record actual results.
4. Exercise the primary success path and at least one validation/error path.
5. Verify authorization boundaries with a negative test where applicable.
6. Check logs for useful context without exposing secrets or personal data.
7. Review configuration defaults, dependency declarations, and ignored files.
8. Confirm that the demo can be repeated without manual database or environment fixes.

## Suggested 3–5 minute demo

1. Introduce the problem and intended users.
2. Show the main workflow through the documented API or interface.
3. Demonstrate input validation and a client-safe error response.
4. Show a relevant test and the observed passing result.
5. Explain one architectural decision, one trade-off, and one known limitation.

## Release readiness scorecard

| Area | Status | Evidence / follow-up |
|---|---|---|
| Setup reproducibility | | |
| Core workflow | | |
| Tests and quality checks | | |
| API and data documentation | | |
| Security and configuration | | |
| Logs and troubleshooting | | |
| Demo script | | |

## Final guardrails

- Report test outcomes only after running the commands.
- Keep secrets in environment configuration, never in source control.
- Distinguish implemented features from planned enhancements.
- Prefer a small, stable demo over an unverified last-minute feature.
