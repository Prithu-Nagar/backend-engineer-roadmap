"""
Day 26 — URL Shortener FastAPI Comparison Implementation

A small FastAPI version of the URL Shortener API is kept beside the existing
Django/DRF implementation so the frameworks can be compared without replacing
the roadmap's current project code.

Day 27 — URL Shortener FastAPI Validation and Dependency Injection

The FastAPI comparison implementation is extended with explicit request and
response models and small dependencies for request context and storage.

Day 28 — URL Shortener Async Endpoint

The FastAPI comparison implementation now includes an async list endpoint.
The endpoint yields to the event loop so the example demonstrates the async
request model without introducing an external service dependency.

Day 29 — URL Shortener Complete Test Suite

The project adds a FastAPI-focused pytest suite covering request validation,
successful create/list/retrieve flows, error responses, and dependency
overrides for isolated test state.

The existing Django/DRF implementation remains the persistent project source
of truth.
"""

import asyncio
import secrets
import string
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field, HttpUrl


app = FastAPI(title="URL Shortener - FastAPI Comparison")

SHORT_CODE_ALPHABET = string.ascii_letters + string.digits


class CreateURLRequest(BaseModel):
    """Validated request body for creating a short URL."""

    original_url: Annotated[HttpUrl, Field(description="Destination URL")]


class ShortURLResponse(BaseModel):
    """Stable response contract for URL records."""

    short_code: str
    short_url: str
    original_url: HttpUrl


class RequestContext(BaseModel):
    """Small request-scoped dependency model."""

    request_id: str | None = None


url_store: dict[str, ShortURLResponse] = {}


def get_request_context(
    request_id: Annotated[str | None, Header()] = None,
) -> RequestContext:
    """Provide request-scoped data through dependency injection."""
    return RequestContext(request_id=request_id)


def get_url_store() -> dict[str, ShortURLResponse]:
    """Provide the URL store through dependency injection."""
    return url_store


@app.post(
    "/api/urls",
    response_model=ShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    payload: CreateURLRequest,
    context: RequestContext = Depends(get_request_context),
    store: dict[str, ShortURLResponse] = Depends(get_url_store),
) -> ShortURLResponse:
    """Create a short URL using validation and injected dependencies."""
    del context

    for _ in range(10):
        short_code = "".join(
            secrets.choice(SHORT_CODE_ALPHABET) for _ in range(6)
        )

        if short_code not in store:
            short_url = ShortURLResponse(
                short_code=short_code,
                short_url=f"http://localhost:8000/{short_code}",
                original_url=payload.original_url,
            )
            store[short_code] = short_url
            return short_url

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Unable to generate a unique short code.",
    )


@app.get("/api/urls", response_model=list[ShortURLResponse])
async def list_short_urls(
    store: dict[str, ShortURLResponse] = Depends(get_url_store),
) -> list[ShortURLResponse]:
    """Return the URL collection from an async FastAPI endpoint."""
    await asyncio.sleep(0)
    return list(store.values())


@app.get("/{short_code}", response_model=ShortURLResponse)
def get_short_url(
    short_code: str,
    store: dict[str, ShortURLResponse] = Depends(get_url_store),
) -> ShortURLResponse:
    """Retrieve a short URL by its generated code."""
    record = store.get(short_code)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found.",
        )

    return record
