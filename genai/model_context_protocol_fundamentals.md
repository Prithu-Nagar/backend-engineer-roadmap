# Model Context Protocol (MCP) Fundamentals

Day 57 introduces the Model Context Protocol (MCP) as a structured way for AI
applications to discover and interact with external tools and resources.

The focus is the protocol boundary and its client/server flow rather than a
specific SDK implementation.

---

## Why MCP Exists

An AI application may need access to capabilities outside the model:

- Databases
- Files
- APIs
- Internal services
- Documentation
- Business workflows

Without a common boundary, each model application can develop a different
integration format.

MCP provides a standardized protocol model for connecting clients with servers
that expose capabilities.

---

## Core Participants

```text
User
  |
  v
AI Application / Host
  |
  v
MCP Client
  |
  | protocol messages
  v
MCP Server
  |
  +---- Tools
  |
  +---- Resources
  |
  +---- Prompts / other supported capabilities
  |
  v
External Systems
```

The exact transport and SDK details depend on the implementation, but the
important architectural boundary is client-to-server capability discovery and
invocation.

---

## Client / Server Flow

A simplified flow is:

```text
1. Client connects to server
2. Client and server establish protocol capabilities
3. Client discovers available capabilities
4. Client selects an approved tool or resource
5. Client sends a structured request
6. Server validates and executes the request
7. Server returns a structured result
```

The client should not assume that every discovered capability is safe or
authorized for every user.

---

## Tools

A tool represents an operation.

A tool definition typically needs:

- Name
- Description
- Input schema
- Application-specific metadata

Example:

```json
{
  "name": "search_orders",
  "description": "Search orders for the current tenant",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"}
    },
    "required": ["query"]
  }
}
```

The application remains responsible for validating arguments and enforcing
authorization.

---

## Resources

A resource represents information identified through a resource URI or
equivalent identifier.

Conceptually:

```text
resource://documentation/backend/authentication
```

A resource can provide structured or textual information to the client while
keeping the underlying storage implementation behind the server boundary.

---

## Discovery

Discovery lets a client learn which capabilities a server exposes.

```text
MCP Server
    |
    +--> Tool definitions
    |
    +--> Resource definitions
    |
    +--> Capability information
```

Discovery does not replace authorization. A capability can be discoverable but
still require user, tenant, or operation-level permission checks.

---

## Security Model

An MCP-enabled application should establish clear trust boundaries.

Important controls include:

- Authentication of the client/server connection
- Capability allowlists
- Tool argument validation
- User and tenant authorization
- Least-privilege credentials
- Timeouts and cancellation
- Audit logging
- Sensitive-data filtering
- Output validation where needed

Never treat model-generated tool arguments as trusted input.

---

## MCP in a Backend Architecture

```text
                    +------------------+
                    | AI Application   |
                    +--------+---------+
                             |
                         MCP Client
                             |
                    +--------v---------+
                    |   MCP Server     |
                    +---+----------+---+
                        |          |
                      Tools     Resources
                        |          |
                        v          v
                  App Services  Read Models
```

The MCP layer should be an adapter around application capabilities rather than
a replacement for normal service boundaries.

---

## MCP vs Direct API Integration

| Concern | Direct API integration | MCP-style integration |
| --- | --- | --- |
| Capability discovery | Application-specific | Protocol-oriented |
| Tool metadata | Custom contract | Standardized capability model |
| Resource access | API-specific | Resource-oriented boundary |
| Model integration | Usually bespoke | Client can discover capabilities |
| Authorization | Application-owned | Still application-owned |

MCP does not remove the need for ordinary API design, authentication,
authorization, observability, or reliability engineering.

---

## Interview Takeaways

- MCP provides a protocol boundary between AI clients and external
  capabilities.
- Servers can expose tools and resources with explicit metadata.
- Clients can discover capabilities before using them.
- Tool execution must remain application-controlled.
- Authentication and authorization remain necessary.
- MCP can reduce repeated bespoke integration patterns without eliminating
  backend engineering concerns.
