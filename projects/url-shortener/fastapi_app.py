"""
Day 26 — URL Shortener FastAPI Comparison Implementation

A small FastAPI version of the URL Shortener API is kept beside the existing
Django/DRF implementation so the frameworks can be compared without replacing
the roadmap's current project code.
"""

import secrets
import string
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from pydantic import BaseModel, HttpUrl


app = FastAPI(title="URL Shortener - FastAPI Comparison")

SHORT_CODE_ALPHABET = string.ascii_letters + string.digits


class CreateURLRequest(BaseModel):
    original_url: HttpUrl


class ShortURLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: HttpUrl


class RequestContext(BaseModel):
    request_id: str | None = None


def get_request_context(
    request_id: Annotated[str | None, Query()] = None,
) -> RequestContext:
    """Provide request-scoped data through FastAPI dependency injection."""

    return RequestContext(request_id=request_id)


url_store: dict[str, ShortURLResponse] = {}


@app.post(
    "/api/urls",
    response_model=ShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_short_url(
    payload: CreateURLRequest,
    context: RequestContext = Depends(get_request_context),
) -> ShortURLResponse:
    """Create a short URL using FastAPI request validation."""

    del context

    for _ in range(10):
        short_code = "".join(
            secrets.choice(SHORT_CODE_ALPHABET) for _ in range(6)
        )
        if short_code not in url_store:
            short_url = ShortURLResponse(
                short_code=short_code,
                short_url=f"http://localhost:8000/{short_code}",
                original_url=payload.original_url,
            )
            url_store[short_code] = short_url
            return short_url

    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Unable to generate a unique short code.",
    )


@app.get("/api/urls", response_model=list[ShortURLResponse])
def list_short_urls() -> list[ShortURLResponse]:
    """Return the in-memory URL collection."""

    return list(url_store.values())


@app.get("/{short_code}", response_model=ShortURLResponse)
def get_short_url(short_code: str) -> ShortURLResponse:
    """Retrieve a short URL by its generated code."""

    record = url_store.get(short_code)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found.",
        )

    return record
