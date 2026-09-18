# Failure Scenarios, Rollback & Recovery Runbook

Day 49 covers production failure handling as a system-design capability.

## Failure Scenarios

### Application Failure

**Symptoms**

- Rising 5xx responses
- Increased request latency
- Failed health checks

**Initial actions**

1. Confirm the affected endpoints and time window.
2. Compare the failure with the latest deployment.
3. Check application logs, metrics, and traces.
4. If the deployment is the likely trigger, prepare a rollback.

### Database Failure

**Symptoms**

- Connection timeouts
- Increased lock waits
- Transaction failures
- Readiness failures

**Initial actions**

1. Check database connectivity and active sessions.
2. Inspect lock blockers and long-running transactions.
3. Confirm whether the application has exhausted its connection budget.
4. Protect the database from additional load before making risky changes.

### Dependency Failure

**Symptoms**

- Timeout or error spikes from a downstream service
- Increased retry volume
- Request latency growth

**Initial actions**

1. Confirm the dependency-specific error rate.
2. Stop unbounded retries.
3. Use cached or degraded behavior if the application supports it.
4. Restore normal traffic only after dependency health is verified.

## Rollback Decision

Rollback is a mitigation option when a recent change correlates strongly with
the incident and the previous version is known to be recoverable.

Before rollback:

- Confirm the deployment version.
- Check database compatibility.
- Preserve incident evidence.
- Confirm that rollback will not remove required schema changes.

After rollback:

- Verify liveness and readiness.
- Check error rate and latency.
- Verify critical user flows.
- Continue monitoring for a defined observation window.

## Recovery Modes

A service can use a controlled degraded mode when full functionality is not
available.

Examples:

- Serve cached reads.
- Disable a non-critical feature.
- Reduce expensive background work.
- Temporarily reject low-priority requests.
- Queue work for later processing.

Recovery mode must be explicit, observable, and reversible.

## Incident Runbook

### 1. Detect

- Alert fires or users report a failure.
- Record the incident start time.
- Create an incident identifier.

### 2. Assess

- Identify affected components.
- Estimate blast radius.
- Check recent deployments and configuration changes.
- Collect logs, metrics, traces, and database evidence.

### 3. Mitigate

Choose the least risky effective action:

- Roll back a deployment.
- Reduce traffic.
- Disable a non-critical feature.
- Isolate a failing dependency.
- Enter a documented recovery mode.

### 4. Recover

- Restore the normal request path.
- Verify health checks.
- Validate critical workflows.
- Monitor error rate, latency, and resource usage.

### 5. Review

Record:

- Trigger
- Root cause
- Contributing factors
- Detection gap
- Mitigation
- Recovery evidence
- Follow-up actions
- Runbook improvements

## Failure Simulation

The Expense Tracker uses controlled failure simulation to exercise the runbook
without depending on an actual production outage.

The simulation should verify:

- Failure detection
- Mitigation selection
- Recovery-mode entry and exit
- Rollback decision recording
- Health verification
- Incident timeline capture
