# Deployment Strategies

Deployment strategy determines how a new application version is introduced while
controlling availability and rollback risk.

---

## Rolling Deployment

Instances are replaced gradually rather than all at once.

```text
v1 v1 v1 v1
   |
   v
v2 v1 v1 v1
   |
   v
v2 v2 v1 v1
   |
   v
v2 v2 v2 v2
```

**Advantages**

- Uses existing capacity.
- Avoids an all-at-once cutover.
- Works well for stateless services.

**Trade-off**

Two application versions may run simultaneously, so API and database changes
must remain compatible during the transition.

---

## Blue/Green Deployment

Two environments are maintained:

```text
             +--> Blue (current)
Traffic -----|
             +--> Green (new)
```

Traffic is switched to the new environment after validation.

**Advantages**

- Fast traffic cutover.
- Simple rollback by switching traffic back.
- Strong separation between current and candidate versions.

**Trade-off**

Running two environments can increase infrastructure cost.

---

## Canary Deployment

A small percentage of traffic is sent to the new version first.

```text
100% traffic
     |
     +----> 95% v1
     |
     +---->  5% v2  <-- observe
```

If metrics remain healthy, the percentage can be increased gradually.

**Advantages**

- Limits blast radius.
- Real production traffic provides feedback.
- Supports metric-driven rollout decisions.

**Trade-off**

Requires reliable routing, monitoring, and rollback automation.

---

## Comparison

| Strategy | Rollout | Rollback | Main Cost |
|---|---|---|---|
| Rolling | Gradual instance replacement | Replace/redeploy previous version | Version compatibility |
| Blue/Green | Traffic switch | Switch traffic back | Duplicate environments |
| Canary | Gradual traffic percentage | Reduce traffic to new version | Strong observability |

---

## Database Compatibility

Deployment strategy does not remove database migration risk. Prefer an
expand-and-contract sequence:

1. Add backward-compatible schema changes.
2. Deploy code that can work with both versions.
3. Backfill or migrate data safely.
4. Switch reads/writes to the new representation.
5. Remove obsolete schema elements only after old code is gone.
