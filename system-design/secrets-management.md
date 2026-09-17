# Secrets Management

Secrets management is the system-design practice of controlling sensitive
configuration such as API keys, database credentials, signing keys, and
service tokens.

## Core Principles

- Keep secrets out of source control.
- Inject secrets at runtime rather than hard-coding them into images.
- Give each service only the secrets it needs.
- Separate development, staging, and production secret stores.
- Rotate credentials when exposure or policy requires it.
- Audit secret access without logging secret values.
- Prefer short-lived credentials when the platform supports them.

## Secret Flow

```text
Secret Store
     |
     v
Deployment / Workload Identity
     |
     v
Application Runtime
     |
     +----> Database / External API
```

The application should receive a secret through a controlled runtime boundary.
The repository and container image should contain configuration structure, not
the secret value itself.

## Common Storage Choices

### Environment Variables

Useful for simple deployments and containerized applications.

Advantages:

- Easy to inject at runtime
- Supported by most deployment platforms
- Keeps values outside source code

Limitations:

- Access can be broader than intended
- Rotation and auditing depend on the platform
- Care is required to prevent accidental logging

### Managed Secret Stores

A cloud or infrastructure secret manager can provide centralized storage,
access policies, rotation workflows, and audit events.

The application normally authenticates using a workload identity or another
deployment-provided identity rather than storing a second long-lived
credential.

## Access Model

```text
                +----------------+
                |   Secret Store |
                +-------+--------+
                        |
                 Access Policy
                        |
          +-------------+-------------+
          |                           |
     Service A                    Service B
     secret A                    secret B
```

Use service-specific access policies. A service that only needs a database
password should not automatically receive unrelated API keys.

## Rotation

A rotation workflow should consider:

1. Create a new credential.
2. Make the application capable of accepting the new credential.
3. Switch traffic or configuration to the new value.
4. Verify successful use.
5. Revoke the old credential.
6. Record the rotation event without recording the secret.

For credentials used by multiple services, use a staged rotation so that
clients do not fail because one side changed before the other.

## What Not to Store

Do not commit:

- Passwords
- API keys
- Private keys
- JWT signing secrets
- Database connection strings containing credentials
- Production `.env` files
- Cloud access tokens

Example:

```text
SECRET_KEY=...
DATABASE_URL=postgresql://...
THIRD_PARTY_API_KEY=...
```

The placeholder names are configuration contracts; the real values belong in
the deployment secret mechanism.

## Security Boundaries

Secrets should cross as few trust boundaries as practical.

A useful review asks:

- Who can read this secret?
- Which service account or workload identity receives it?
- Can the secret appear in logs, traces, crash reports, or error messages?
- How is access audited?
- How is the secret rotated or revoked?
- What happens if one service is compromised?

## Relationship to Day 47

Day 47 introduced security boundaries and threat modeling. Day 48 adds the
operational secret-management model that supports those boundaries.

Together, the controls reduce the chance that credentials are accidentally
stored in source code, broadly shared between services, or exposed through
operational telemetry.
