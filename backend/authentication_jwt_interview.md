# Authentication and JWT — Backend Interview Questions

Use these questions to practice describing a secure request flow, token lifecycle, and framework-specific implementation trade-offs.

## Core Questions

### 1. Authentication vs authorization
Authentication establishes who the caller is. Authorization decides whether that identity may perform a particular action on a resource. Every protected endpoint needs the appropriate authorization check, not just a successful login.

### 2. What is a JWT?
A JSON Web Token is a compact claims representation. A signed JWT commonly has a header, payload, and signature. Base64url encoding is not encryption: claims may be readable by anyone holding the token.

### 3. What must be validated?
- Verify the signature with an explicitly allowed algorithm and trusted key.
- Validate issuer (`iss`), audience (`aud`), expiration (`exp`), and not-before (`nbf`) when applicable.
- Apply a small, deliberate clock-skew allowance.
- Reject malformed tokens and unexpected algorithms; do not trust token-provided key URLs without a controlled trust policy.
- Validate scopes/roles and resource ownership separately from token validity.

### 4. Access tokens vs refresh tokens
Access tokens should be short-lived and sent only over protected channels. Refresh tokens need stronger lifecycle controls, secure storage, rotation, and revocation/reuse detection where supported. Do not place long-lived secrets in browser-accessible storage without evaluating XSS and CSRF risks.

### 5. Where should tokens be stored?
The answer depends on client type and threat model. Browser cookies marked `Secure`, `HttpOnly`, and an appropriate `SameSite` policy reduce JavaScript access but require CSRF analysis. Bearer tokens in browser storage are exposed to script running in the origin. Mobile and server clients have different secure-storage options.

### 6. How do you revoke a JWT?
Self-contained access tokens are not automatically revocable before expiry. Options include short lifetimes, token-version checks, deny lists, session records, or key rotation, each with availability and operational trade-offs. Refresh-token rotation is commonly used to limit long-lived access.

### 7. How should passwords be stored?
Use a purpose-built password hashing function such as Argon2id, scrypt, or bcrypt with unique salts and appropriate work factors. Never store plaintext passwords or use a fast general-purpose hash such as plain SHA-256 for password storage.

## Request Flow

1. Validate credentials and apply login rate limits.
2. Create a short-lived access token with minimal claims and a refresh mechanism appropriate to the client.
3. Validate signature and standard claims on protected requests.
4. Apply authorization policy to the requested action and resource.
5. Audit security-relevant events without logging credentials, full tokens, or sensitive claims.
6. Rotate signing keys with a documented overlap and rollback strategy.

## Framework Interview Prompts

- **Flask:** Where do authentication middleware/decorators live, and how are request-local identities handled?
- **Django/DRF:** How do authentication classes differ from permission classes? How do you enforce object-level permissions?
- **FastAPI:** How do dependency-based security checks compose, and how are scopes represented?
- How would you test expired tokens, wrong audience, key rotation, revoked refresh tokens, and unauthorized resource access?

## Common Mistakes

- Treating JWT payloads as encrypted secrets.
- Accepting an arbitrary algorithm or skipping audience/issuer validation.
- Treating authentication as sufficient authorization.
- Putting passwords, API keys, or unnecessary personal data in claims.
- Logging bearer tokens or returning detailed authentication failures that enable account enumeration.
- Forgetting rate limits, secure transport, key management, and token expiry.
