"""
Day 27 — FastAPI Validation and Response Models

FastAPI uses Python type hints and Pydantic models to validate incoming data
and document the API contract automatically.
"""

from typing import Annotated

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field


app = FastAPI(title="FastAPI Validation")


class CreateURLRequest(BaseModel):
    """Validated request body for a URL-shortening operation."""

    original_url: str = Field(min_length=1, max_length=2048)


class URLResponse(BaseModel):
    """Stable response contract for URL data."""

    short_code: str
    short_url: str
    original_url: str


@app.post("/api/urls", response_model=URLResponse)
def create_url(payload: CreateURLRequest) -> URLResponse:
    """Validate input and return a documented response model."""
    short_code = "demo123"

    return URLResponse(
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        original_url=payload.original_url,
    )


@app.get("/api/urls/{short_code}", response_model=URLResponse)
def get_url(
    short_code: Annotated[str, Path(min_length=1, max_length=20)],
    include_metadata: Annotated[bool, Query()] = True,
) -> URLResponse:
    """Demonstrate path and query validation with a response model."""
    del include_metadata

    return URLResponse(
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        original_url="https://example.com",
    )
