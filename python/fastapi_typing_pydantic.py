"""
Day 27 — FastAPI Typing and Pydantic Models

This example demonstrates how Python type hints and Pydantic models make
FastAPI request and response contracts explicit.
"""

from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


app = FastAPI(title="FastAPI Typing and Pydantic")


class TaskCreate(BaseModel):
    """Request model for creating a task."""

    title: Annotated[str, Field(min_length=1, max_length=200)]
    completed: bool = False
    priority: Annotated[int, Field(ge=1, le=5)] = 3


class TaskResponse(BaseModel):
    """Response model returned by the API."""

    id: int
    title: str
    completed: bool
    priority: int


@app.post("/tasks", response_model=TaskResponse)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Validate a request body and return a typed response."""
    return TaskResponse(
        id=1,
        title=payload.title,
        completed=payload.completed,
        priority=payload.priority,
    )


@app.get("/tasks")
def list_tasks(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, object]:
    """Demonstrate typed query-parameter validation."""
    return {"items": [], "limit": limit}
