# AI-Enabled Backend Architecture

Day 51 introduces an architecture for adding LLM capabilities to a backend
without allowing model-specific concerns to leak across the whole service.

---

## Core Flow

```text
Client
  |
  v
API / Authentication
  |
  v
Application Service
  |
  +----> Validation / Policy
  |
  v
AI Orchestration Layer
  |
  +----> Prompt construction
  +----> Model client
  +----> Output parsing
  |
  v
External LLM Provider
```

The backend remains responsible for authentication, authorization, validation,
timeouts, logging, rate limiting, and error handling.

---

## Recommended Boundaries

### API Layer

Responsible for:

- Request validation
- Authentication and authorization
- Rate limiting
- API response contracts
- Request identifiers

### Application Service

Responsible for:

- Business rules
- Selecting the AI workflow
- Combining user context with application data
- Handling domain-level failures

### AI Orchestration

Responsible for:

- Prompt templates
- Model selection
- Structured output parsing
- Retrieval or tool orchestration
- Provider abstraction

### Model Client

Responsible for:

- HTTP/API interaction
- API credentials
- Timeouts
- Provider-specific request and response mapping

---

## Reliability Controls

LLM calls should be treated as external dependency calls.

Useful controls include:

- Explicit connect/read timeouts
- Bounded retries for retryable failures
- Rate limiting
- Circuit breaking where appropriate
- Response-schema validation
- Maximum input and output sizes
- Token and cost budgets
- Structured error handling
- Fallback behavior for dependency failure

Retries should not blindly repeat non-idempotent downstream operations.

---

## Data Flow

```text
User Request
     |
     v
Validate + Authorize
     |
     v
Build AI Input
     |
     +----> Optional retrieval
     |
     v
LLM Provider
     |
     v
Validate Output
     |
     v
Business Logic
     |
     v
API Response
```

The application should validate model output before treating it as trusted
application data.

---

## Observability

Track operational metrics such as:

- Request count
- LLM latency
- Error rate
- Timeout rate
- Input/output token usage when available
- Estimated cost
- Retry count
- Model/provider used

Avoid logging prompts or responses when they contain sensitive user data.

---

## Key Trade-offs

| Concern | Centralized AI Layer | AI Logic in Every Service |
|---|---|---|
| Consistency | Higher | Lower |
| Provider changes | Easier | Repeated work |
| Service autonomy | Lower | Higher |
| Governance | Easier | Harder |
| Initial simplicity | Moderate | Appears simpler |

The appropriate boundary depends on service ownership, scale, and how widely AI
capabilities are shared across the system.
