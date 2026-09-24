# Agent Architecture

Day 55 introduces an architecture for AI agents that can plan work, call
bounded tools, maintain state, and enforce guardrails.

The key design principle is that the model proposes actions while the
application controls authorization, validation, execution, and limits.

---

## High-Level Architecture

```text
Client
  |
  v
Agent API
  |
  v
Agent Orchestrator
  |
  +--------------------+
  |                    |
  v                    v
State Store          LLM
  |                    |
  |                    +----> Tool Decision
  |                              |
  |                              v
  |                       Tool Policy / Guardrails
  |                              |
  |                              v
  |                       Tool Executor
  |                              |
  |              +---------------+---------------+
  |              |               |               |
  |              v               v               v
  |           Database       Internal API    External API
  |              |               |               |
  +--------------+---------------+---------------+
                         |
                         v
                    Tool Result
                         |
                         v
                        LLM
                         |
                         v
                    Final Response
```

---

## Agent Components

### Agent Orchestrator

The orchestrator owns the control loop.

Responsibilities include:

- Receiving the user request
- Loading relevant state
- Calling the model
- Validating tool requests
- Executing allowed tools
- Recording tool results
- Enforcing iteration and timeout limits
- Returning the final response

### Model

The model is responsible for language understanding and action selection.

The model should not directly access:

- Database connections
- Application secrets
- Filesystem APIs
- Arbitrary network clients
- Unrestricted Python execution

### Tool Registry

The registry defines the tools available to the agent.

Each tool should have:

- Name
- Description
- Input schema
- Output contract
- Authorization rules
- Timeout
- Audit requirements

### State Store

State can contain:

- Conversation messages
- Tool calls
- Tool results
- User/session identifiers
- Task progress
- Iteration counters

Possible implementations include:

- In-memory state for simple workflows
- Redis for low-latency shared state
- PostgreSQL for durable state
- Workflow persistence for long-running agents

---

## Agent Loop

```text
Receive request
      |
      v
Load state
      |
      v
Call model
      |
      v
Final response? ---- Yes ---> Return
      |
      No
      |
      v
Validate tool request
      |
      v
Authorized?
   /        No         Yes
 |           |
Reject       v
         Execute tool
             |
             v
        Record result
             |
             v
          Update state
             |
             v
          Call model
```

---

## Planning

Planning can be explicit or implicit.

### Implicit Planning

The model decides the next action one step at a time.

```text
Request
  |
  v
Model
  |
  v
Tool
  |
  v
Result
  |
  v
Model
```

### Explicit Planning

The agent first creates a bounded plan.

```text
Request
  |
  v
Planner
  |
  v
Plan
  |
  +--> Step 1
  +--> Step 2
  +--> Step 3
  |
  v
Final response
```

Explicit planning can make multi-step workflows easier to observe, but it
also introduces additional state and validation requirements.

---

## Guardrails

Guardrails should be enforced outside the model.

Important controls include:

- Tool allowlists
- Authentication
- Authorization
- Input validation
- Resource ownership checks
- Rate limits
- Timeouts
- Maximum iterations
- Payload limits
- Sensitive-data filtering
- Audit logging

A rejected tool call should not be treated as successful execution.

---

## Failure Handling

Common failure modes include:

| Failure | Handling |
|---|---|
| Invalid tool name | Reject before execution |
| Invalid arguments | Validate against schema |
| Unauthorized action | Reject and audit |
| Tool timeout | Cancel or retry within policy |
| Tool failure | Record error and decide whether to retry |
| Model loop | Enforce maximum iterations |
| State-store failure | Fail safely and preserve audit data when possible |

Retries should be applied only to operations where retrying is safe.

---

## Stateful vs Stateless Agent Services

A stateless API can keep durable conversation and tool state in an external
store:

```text
Client
  |
  v
Load Balancer
  |
  +------> Agent Instance A
  |
  +------> Agent Instance B
             |
             v
        Shared State Store
```

This allows multiple service instances to handle requests for the same user
session.

A stateful in-process design can be simpler for prototypes but makes
horizontal scaling and failover more difficult.

---

## Security Boundary

The most important boundary is:

```text
LLM decision
     |
     v
Application policy
     |
     v
Tool execution
```

The LLM can request an action, but the application determines whether that
action is valid and permitted.

---

## Observability

Agent systems should record:

- Agent run ID
- Session ID
- Model identifier
- Tool name
- Tool-call status
- Request timestamp
- Execution duration
- Error code
- Retry count
- Token usage when available

Avoid storing sensitive payloads unnecessarily. Redaction and retention
policies should be applied to tool arguments and results.

---

## Interview Checklist

- What is the agent control loop?
- Where is tool authorization enforced?
- How is agent state stored?
- How are tool calls validated?
- How do you stop an infinite agent loop?
- How are tool failures handled?
- How do you make agent execution observable?
- How do you scale stateless agent workers?
- Which operations are safe to retry?
