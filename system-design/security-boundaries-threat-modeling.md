# Security Boundaries & Threat Modeling

Security boundaries define where trust changes between clients, services,
databases, and external dependencies. Threat modeling makes those boundaries
explicit before an incident exposes a weakness.

## Trust Boundaries

Typical boundaries in a backend service include:

```text
Internet Client
      |
      v
+-------------------+
| Reverse Proxy /   |
| API Gateway       |
+-------------------+
      |
      v
+-------------------+
| Application       |
| Service           |
+-------------------+
   |           |
   v           v
Database      Redis
   |
   v
External Services
```

Treat each boundary as untrusted until the receiving component validates the
input and verifies the caller's authorization.

## Threat Modeling Questions

For each important flow, ask:

1. What assets need protection?
2. Who can send input across the boundary?
3. What authentication establishes identity?
4. What authorization permits the requested action?
5. What data crosses the boundary?
6. What happens if the dependency is compromised or unavailable?
7. What should be logged without exposing secrets?
8. How can the system detect and contain abuse?

## Common Threat Categories

### Spoofing

An attacker attempts to impersonate a user or service.

Controls include:

- Strong authentication
- Short-lived access tokens
- Secure credential storage
- Service-to-service authentication

### Tampering

An attacker attempts to alter data or requests.

Controls include:

- TLS
- Request validation
- Authorization checks
- Integrity checks where appropriate

### Information Disclosure

Sensitive information is exposed through responses, logs, errors, or overly
broad database access.

Controls include:

- Least-privilege database roles
- Secret management
- Redacted logs
- Safe error responses

### Denial of Service

An attacker consumes excessive application or dependency resources.

Controls include:

- Rate limiting
- Request-size limits
- Timeouts
- Bounded concurrency
- Dependency isolation

## Security Boundary Checklist

- Authenticate at the appropriate boundary.
- Authorize every protected operation.
- Validate untrusted input before use.
- Keep secrets out of source control and logs.
- Use explicit CORS allow-lists.
- Protect cookie-authenticated state-changing requests against CSRF.
- Use least-privilege database roles.
- Return generic errors to clients while retaining useful internal diagnostics.
- Monitor authentication failures and suspicious access patterns.
- Define incident response and credential-rotation procedures.
