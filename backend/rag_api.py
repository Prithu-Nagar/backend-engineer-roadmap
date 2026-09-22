"""
Day 53 — RAG API Design

A provider-neutral FastAPI boundary for a retrieval-augmented generation
request. Retrieval, reranking, and generation remain behind explicit
interfaces so the HTTP layer stays small and testable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class RagRequest(BaseModel):
    query: str = Field(min_length=1)
    tenant_id: int = Field(gt=0)
    top_k: int = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    chunk_id: int
    score: float
    text: str


class RagResponse(BaseModel):
    answer: str
    sources: list[Source]


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: int
    text: str
    score: float


class RagService(Protocol):
    async def answer(
        self,
        query: str,
        tenant_id: int,
        top_k: int,
    ) -> RagResponse: ...


class DemoRagService:
    """Small deterministic implementation for demonstrating the API boundary."""

    async def answer(
        self,
        query: str,
        tenant_id: int,
        top_k: int,
    ) -> RagResponse:
        source = Source(
            chunk_id=1,
            score=0.91,
            text=f"Demo context selected for tenant {tenant_id}.",
        )
        return RagResponse(
            answer=f"Retrieved context can now be used to answer: {query}",
            sources=[source][:top_k],
        )


app = FastAPI(title="RAG API Example")
rag_service: RagService = DemoRagService()


@app.post("/rag/query", response_model=RagResponse)
async def rag_query(request: RagRequest) -> RagResponse:
    try:
        return await rag_service.answer(
            query=request.query,
            tenant_id=request.tenant_id,
            top_k=request.top_k,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
