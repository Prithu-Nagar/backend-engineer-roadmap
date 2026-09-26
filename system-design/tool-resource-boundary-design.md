# Tool / Resource Boundary Design

Day 57 defines the architectural boundary between an MCP-style protocol layer
and the application capabilities exposed through it.

The key idea is to expose explicit, approved capabilities rather than allowing
a model or external client to directly access arbitrary application internals.

---

## Boundary Model

```text
MCP Client
    |
    v
MCP Protocol Adapter
    |
    +-------------------+
    |                   |
    v                   v
Tool Registry       Resource Registry
    |                   |
    v                   v
Application Services  Read Models / Stores
```

The protocol adapter translates protocol requests into application-owned
operations.

---

## Tool Boundary

A tool represents an operation that can perform work.

Examples:

- Create a task
- Search records
- Calculate a value
- Trigger an approved workflow

A tool boundary should define:

- Stable name
- Description
- Input schema
- Authorization requirements
- Validation rules
- Execution timeout
- Error contract
- Audit metadata

The tool should call an application service rather than reaching directly into
an arbitrary database or internal module.

---

## Resource Boundary

A resource represents information that can be read through a defined URI or
resource identifier.

Examples:

- Configuration metadata
- Documentation
- Read-only application state
- Tenant-scoped reference data

Resource boundaries should define:

- Stable URI
- Ownership
- Read permissions
- Data classification
- Serialization format
- Cache policy where appropriate

Resources should be narrower than unrestricted database access.

---

## Tool vs Resource

| Concern | Tool | Resource |
| --- | --- | --- |
| Primary purpose | Perform an operation | Expose information |
| Typical effect | May change state | Usually read-only |
| Input | Arguments | Resource URI |
| Authorization | Action permission | Read permission |
| Audit | Execution record | Access record when required |
| Failure | Tool execution error | Resource read error |

The distinction helps keep application behavior explicit.

---

## Authorization Boundary

```text
Request
   |
   v
Authenticate
   |
   v
Authorize capability
   |
   +---- denied ----> Error
   |
   v
Validate arguments / URI
   |
   v
Application service or read model
```

Authorization should happen before executing a tool or returning protected
resource data.

Tenant and user context should be derived from trusted request context rather
than accepting arbitrary tenant identifiers from model-generated arguments.

---

## Reliability Boundary

Protocol-level timeouts should not be the only protection.

A tool boundary can enforce:

- Per-tool timeout
- Request cancellation
- Retry policy for safe operations
- Idempotency for retried mutations
- Concurrency limits
- Circuit breaking for unstable dependencies
- Structured error mapping

Long-running work can be converted into a job-oriented workflow rather than
holding a protocol request open indefinitely.

---

## Observability

Record enough metadata to reconstruct an execution without storing sensitive
arguments unnecessarily.

Useful fields include:

- Request or trace ID
- Server identifier
- Tool/resource name
- Tenant identifier
- Start and completion time
- Outcome
- Error category
- Latency
- Version

Secrets, credentials, and unnecessary sensitive payloads should not be
written to logs.

---

## Scaling

Keep the MCP adapter stateless when possible.

```text
                 +--> MCP Adapter 1 --+
MCP Clients ---->+--> MCP Adapter 2 --+----> Shared Services
                 +--> MCP Adapter 3 --+
```

Shared durable state belongs behind the adapter so instances can scale
horizontally.

Tool execution that requires long-lived state can instead use a job store or
workflow engine with explicit resume semantics.

---

## Design Checklist

Before exposing a capability, verify:

1. Is it an intentional tool or resource?
2. Is its schema stable and explicit?
3. Is authorization defined?
4. Is tenant isolation enforced?
5. Are timeouts and cancellation handled?
6. Is the operation idempotent when retries are possible?
7. Is sensitive data excluded from logs?
8. Can the capability be independently tested?
