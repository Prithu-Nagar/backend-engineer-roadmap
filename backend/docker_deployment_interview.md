# Docker and Deployment — Backend Interview Questions

Use these questions to explain containerization, repeatable deployments, runtime configuration, and production troubleshooting.

## Docker Fundamentals

### 1. What is the difference between an image and a container?
An image is a packaged, largely immutable template containing application files and runtime dependencies. A container is a running instance created from an image with its own runtime configuration and writable layer.

### 2. What makes a good production Docker image?
Use a small trusted base image, pin dependencies deliberately, install only runtime requirements, run as a non-root user, define an appropriate working directory, and avoid copying secrets or local development artifacts. Use a `.dockerignore` file to reduce build context and prevent accidental inclusion.

### 3. Why use multi-stage builds?
Multi-stage builds separate build-time tooling from the final runtime image. This can reduce image size and remove compilers or temporary artifacts from production, while keeping the build reproducible.

### 4. How should configuration and secrets be supplied?
Use environment-specific configuration and an approved secret manager or deployment platform. Do not bake credentials into images, source control, Docker build arguments, or logs. Validate required configuration at startup and fail clearly when it is missing.

## Deployment and Reliability

### 5. What is the difference between readiness and liveness checks?
A liveness check indicates whether the process should be restarted. A readiness check indicates whether it can receive traffic. Readiness may account for required dependencies; liveness should avoid failing merely because a downstream service is temporarily unavailable.

### 6. How do you deploy without dropping requests?
Use rolling or blue-green deployment strategies, health checks, graceful shutdown, connection draining, and backward-compatible schema changes. The exact approach depends on the platform and traffic requirements.

### 7. How should database migrations be handled?
Treat migrations as a controlled release step. Prefer backward-compatible expand-and-contract changes when old and new application versions may run simultaneously. Back up critical data, monitor migration duration, and define a recovery plan before destructive changes.

### 8. What should you monitor after deployment?
Track error rate, latency percentiles, throughput, resource utilization, restart counts, saturation, and dependency health. Compare the new release against a baseline and use a rollback or mitigation plan when service-level objectives are threatened.

## Troubleshooting Scenarios

### 9. A container works locally but fails in production. What do you check?
- Image architecture, runtime version, and dependency versions.
- Environment variables, secret injection, file permissions, and working directory.
- Port binding, network policy, DNS, and dependency connectivity.
- Health-check configuration, CPU/memory limits, and process signals.
- Logs and recent changes, while avoiding exposure of sensitive values.

### 10. Why should containers not store important state only in their writable layer?
Containers can be replaced during deployments, scaling, or recovery. Persist important data in managed storage or databases and treat container filesystems as ephemeral unless the platform explicitly guarantees otherwise.

## Key Takeaways

- Build reproducible, minimal images and run with least privilege.
- Keep configuration separate from the image and protect secrets.
- Use health checks, graceful shutdown, and backward-compatible migrations.
- Verify deployments through observability and a documented rollback plan.
