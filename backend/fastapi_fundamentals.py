"""
Day 26 — FastAPI Fundamentals

A compact example covering routing and dependency injection with FastAPI.
The dependency is deliberately small so the file can be used as a standalone
reference without introducing application-specific database code.
"""

from fastapi import Depends, FastAPI, Query


app = FastAPI(title="FastAPI Fundamentals")


class RequestContext:
    """Small dependency object representing request-scoped context."""

    def __init__(self, request_id: str | None = None) -> None:
        self.request_id = request_id


def get_request_context(
    request_id: str | None = Query(default=None),
) -> RequestContext:
    """Build request context through FastAPI dependency injection."""

    return RequestContext(request_id=request_id)


@app.get("/health")
def health() -> dict[str, str]:
    """Return a simple health response."""

    return {"status": "ok"}


@app.get("/api/urls")
def list_urls(
    context: RequestContext = Depends(get_request_context),
) -> dict[str, object]:
    """Illustrate a dependency-injected API endpoint."""

    return {
        "data": [],
        "meta": {"count": 0, "request_id": context.request_id},
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
