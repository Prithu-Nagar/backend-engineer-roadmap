# Day 90 — Capstone Completion and Portfolio Readiness

## Objective

Close the 90-day roadmap with a truthful, reproducible portfolio artifact. This checklist is a release gate, not a claim that the project is production-ready.

## Functional and technical acceptance

- [ ] Core use cases work from a clean setup using documented instructions.
- [ ] API routes, methods, payloads, response codes, validation, and authorization match the implementation.
- [ ] Database schema, relationships, constraints, indexes, migrations, and transaction boundaries are documented.
- [ ] Error responses are consistent and do not expose secrets, stack traces, or internal details.
- [ ] Configuration comes from environment variables or a documented configuration layer.
- [ ] Dependencies are declared and the project starts without relying on local-only files.
- [ ] Tests cover important success paths, validation failures, authorization boundaries, and persistence behavior.
- [ ] Linting, formatting, and test commands are documented; record results only after running them.
- [ ] Logs, metrics, health checks, and failure handling are appropriate to the project's scope.
- [ ] Docker/Compose and CI workflows, if included, work from a clean checkout.

## README and architecture

- [ ] State the problem, intended users, core features, and explicit non-goals.
- [ ] List the real technology stack and prerequisites.
- [ ] Include copy-pasteable setup, configuration, migration, run, and test commands.
- [ ] Include an API endpoint table and example requests/responses where useful.
- [ ] Add an architecture diagram that matches the current code.
- [ ] Explain important design decisions and trade-offs.
- [ ] Document limitations, troubleshooting, and possible next steps.
- [ ] Remove placeholder claims, dead links, credentials, private identifiers, and unsupported performance claims.

## Demo checklist

1. Introduce the problem and intended users.
2. Demonstrate one primary success workflow.
3. Show validation or authorization failure handling.
4. Show a relevant test and the actual result.
5. Explain one design decision, one trade-off, and one known limitation.

## Portfolio and resume evidence

- [ ] Prepare a concise project summary that describes what was actually built.
- [ ] Use measurable results only when they were measured and can be explained.
- [ ] Link to the repository and a demo only if the links are public and working.
- [ ] Keep the resume focused on contribution, technical decisions, and verified outcomes.
- [ ] Check that no employer/client confidential information or credentials are included.

## Final release scorecard

| Area | Status | Evidence / follow-up |
|---|---|---|
| Reproducible setup | | |
| Core workflow and API contracts | | |
| Tests and quality checks | | |
| Data model and migrations | | |
| Security and configuration | | |
| Observability and failure behavior | | |
| README and architecture | | |
| Demo and portfolio links | | |

## Long-term maintenance plan

- [ ] Schedule weekly DSA practice and a monthly timed benchmark.
- [ ] Revisit Python, SQL, backend, and system design gaps using the scorecards from this roadmap.
- [ ] Keep the capstone working by updating dependencies deliberately and running tests after changes.
- [ ] Add features only when they strengthen a clear use case; avoid adding technology for its own sake.
- [ ] Review the portfolio monthly and keep resume claims aligned with verifiable repository evidence.

## Completion criteria

The capstone is portfolio-ready when its setup is reproducible, documentation matches the implementation, checks have been run and recorded honestly, and the demo can be repeated without hidden manual steps.
