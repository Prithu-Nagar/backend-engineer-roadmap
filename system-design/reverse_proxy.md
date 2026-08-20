# Reverse Proxy

A Reverse Proxy is a server that sits between clients and backend servers.

Instead of clients communicating directly with the backend application,
they communicate with the reverse proxy first.

The reverse proxy then forwards the request to the appropriate backend server.

---

## Why do we need a Reverse Proxy?

- Hides backend servers from clients.
- Improves security.
- Performs load balancing.
- SSL/TLS termination.
- Caching.
- Compression.
- Logging and Monitoring.

---

## Request Flow


Client
   │
   ▼
Reverse Proxy
   │
   ▼
Backend Server

---

## Popular Reverse Proxies

- Nginx
- HAProxy
- Traefik
- Apache HTTP Server
- Envoy Proxy

---

## Advantages

- Better Security
- Improved Performance
- Centralized SSL Management
- Load Distribution
- Easy Scaling

---

## Reverse Proxy vs Forward Proxy

| Reverse Proxy | Forward Proxy |
|---------------|---------------|
| Protects Servers | Protects Clients |
| Used by Server Owners | Used by Clients |
| Client doesn't know backend | Server doesn't know client |

---

## Real-world Examples

- Nginx
- Cloudflare
- AWS Application Load Balancer
- Azure Application Gateway
