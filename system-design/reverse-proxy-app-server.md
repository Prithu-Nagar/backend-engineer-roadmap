# Reverse Proxy + Application Servers

A production web application commonly places a reverse proxy in front of one
or more application-server processes.

```text
Client
  |
  v
Reverse Proxy
  |
  +----------------+----------------+
  |                |                |
  v                v                v
App Server       App Server       App Server
  |                |                |
  +----------------+----------------+
                   |
                   v
              Database / Cache
```

## Reverse Proxy Responsibilities

- Accept public HTTP/HTTPS traffic.
- Terminate TLS when appropriate.
- Route requests to healthy application servers.
- Apply connection, request-size, and timeout policies.
- Support load balancing and centralized access logging.

## Application Server Responsibilities

The application server runs the Python web application through its web-server
interface:

- Flask applications commonly use WSGI servers such as Gunicorn.
- FastAPI applications use ASGI servers such as Uvicorn or an ASGI-compatible
  process manager.

The reverse proxy and application server are separate concerns. The proxy
handles edge traffic, while the application server manages Python application
execution.

## WSGI vs ASGI

| Interface | Typical Python Frameworks | Main Strength |
|---|---|---|
| WSGI | Flask, traditional Django | Synchronous web applications |
| ASGI | FastAPI, async Django | Async I/O and long-lived connections |

## Production Flow

1. Client connects to the public endpoint.
2. Reverse proxy terminates TLS and validates basic request constraints.
3. Proxy forwards the request to a healthy application-server process.
4. Application executes business logic and accesses dependencies.
5. Response returns through the application server and proxy.

## Failure Considerations

- Remove unhealthy application instances from routing.
- Configure upstream timeouts so stalled requests do not consume capacity
  indefinitely.
- Use graceful shutdown so in-flight requests can finish during deployment.
- Keep the application stateless when possible so instances can be replaced.
