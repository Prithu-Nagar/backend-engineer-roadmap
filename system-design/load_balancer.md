# Load Balancer

A Load Balancer distributes incoming client requests across multiple backend servers to improve availability, scalability, and fault tolerance.

---

## Why do we need a Load Balancer?

Without a Load Balancer:

- A single server handles all traffic.
- Server overload can cause slow responses or downtime.
- Scaling the application becomes difficult.

With a Load Balancer:

- Traffic is distributed across multiple servers.
- Failed servers are automatically removed from rotation.
- New servers can be added without affecting clients.

---

## Architecture


              Users
                 │
                 ▼
         +----------------+
         | Load Balancer  |
         +----------------+
          /      |       \
         ▼       ▼        ▼
    Server1  Server2  Server3
          \      |      /
             Database

---

## Benefits

- High Availability
- Scalability
- Fault Tolerance
- Better Performance
- Efficient Resource Utilization

---

## Health Checks

A Load Balancer periodically checks whether backend servers are healthy.

Healthy servers continue receiving traffic.

Unhealthy servers are temporarily removed until they recover.

---

## Load Balancing Algorithms

### Round Robin

Requests are distributed sequentially.


Request 1 → Server A

Request 2 → Server B

Request 3 → Server C

Request 4 → Server A

---

### Least Connections

The next request is routed to the server with the fewest active connections.

Useful when requests have varying execution times.

---

### Weighted Round Robin

Servers receive traffic proportional to assigned weights.

Example:


Server A → Weight 3

Server B → Weight 1

Server A receives approximately three times more requests.

---

### IP Hash

The client IP determines which backend server handles the request.

Useful for sticky sessions.

---

## Layer 4 vs Layer 7

| Layer 4 | Layer 7 |
|----------|----------|
| Transport Layer | Application Layer |
| Uses IP and Port | Uses HTTP/HTTPS |
| Faster | Smarter Routing |
| Cannot inspect URLs | Can inspect URLs |

---

## Sticky Sessions

Sticky Sessions ensure that requests from the same client are consistently routed to the same backend server.

Modern distributed applications typically avoid sticky sessions by storing session data in Redis or a database.

---

## Load Balancer vs Reverse Proxy

| Load Balancer | Reverse Proxy |
|---------------|---------------|
| Distributes traffic | Forwards requests |
| Improves scalability | Hides backend servers |
| Performs health checks | Can cache responses |
| Provides high availability | Provides routing and security |

Tools such as **Nginx** and **HAProxy** can perform both roles.

---

## Common Cloud Load Balancers

- AWS Elastic Load Balancer (ELB)
- Google Cloud Load Balancer
- Azure Load Balancer

---

## Interview Questions

- What is a Load Balancer?
- Why do we need Load Balancing?
- Explain Round Robin.
- Explain Least Connections.
- Difference between Layer 4 and Layer 7 Load Balancers?
- What are Sticky Sessions?
- Difference between Reverse Proxy and Load Balancer?

---

## Summary

- A Load Balancer distributes incoming traffic across multiple servers.
- It improves scalability, availability, and fault tolerance.
- Health checks ensure only healthy servers receive requests.
- Common algorithms include Round Robin, Least Connections, Weighted Round Robin, and IP Hash.
- Layer 7 Load Balancers provide content-aware routing, while Layer 4 Load Balancers operate at the transport layer.