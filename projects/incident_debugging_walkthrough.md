# Incident and Debugging Walkthrough

Use this template to explain a production issue in an interview. Replace the illustrative details with a real incident you personally investigated; do not claim unverified metrics or outcomes.

## 1. Incident Summary

- **Service:** Task Manager API
- **Symptom:** A recent release is followed by increased request failures and latency.
- **Impact:** Determine affected routes, users, duration, and data integrity from evidence.
- **Detection:** Alert, dashboard, support report, or log signal.
- **Severity:** Assign according to customer impact and the team's incident policy.

## 2. Triage and Evidence

1. Confirm the alert and compare current error rate and latency with the baseline.
2. Identify the first occurrence and correlate it with releases, configuration changes, and dependency events.
3. Inspect structured logs using request/correlation IDs; review traces and dependency timings.
4. Check database connectivity, connection-pool saturation, queue depth, and resource utilization.
5. Reproduce with sanitized inputs in a safe environment.
6. Record facts separately from hypotheses.

Do not include credentials, tokens, raw sensitive payloads, or personal data in the incident notes.

## 3. Hypothesis and Mitigation

| Hypothesis | Evidence to collect | Safe validation |
|---|---|---|
| New validation rejects valid requests | Error codes and sanitized request shape | Reproduce against old and new versions |
| Database pool is exhausted | Pool wait time, active connections, slow queries | Compare pool metrics and query timings |
| Downstream service is timing out | Trace spans and dependency error rate | Test dependency health and timeout behavior |
| Release configuration changed | Deployment diff and effective configuration | Verify configuration against known-good values |

Choose mitigation based on evidence: rollback, disable a feature flag, reduce load, or restore a dependency. Assess risks and obtain the required approval before taking production action.

## 4. Recovery Verification

- Confirm error rate and latency return toward the established baseline.
- Verify critical user flows and data consistency.
- Check that queues drain and retries do not amplify load.
- Keep monitoring through an agreed observation window.
- Communicate impact, mitigation, and remaining risk to stakeholders.

## 5. Root Cause and Prevention

Document the causal chain, not just the immediate symptom. Add a regression test, improve validation or timeout behavior, introduce missing metrics or alerts, update the runbook, and assign follow-up owners and due dates.

## 6. Interview Answer Structure

Use a concise sequence: **Situation → Impact → Investigation → Evidence → Mitigation → Verification → Prevention**.

Be clear about your own contribution, the team's contribution, uncertainty, and what you would improve next time. Never invent incident details or numerical impact.
