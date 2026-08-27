"""
Day 27 — LangChain + FastAPI Integration

The example keeps model configuration outside the HTTP route and shows how a
LangChain runnable can be exposed through a typed FastAPI endpoint.

The LangChain import is intentionally local so the file can still be imported
for inspection in environments where LangChain is not installed.
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="LangChain + FastAPI Integration")


class PromptRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class PromptResponse(BaseModel):
    answer: str


def build_chain() -> Any:
    """Build a small LangChain pipeline when the dependency is available."""
    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.runnables import RunnableLambda
    except ImportError as exc:
        raise RuntimeError(
            "Install LangChain Core to run the integration example."
        ) from exc

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a concise backend engineering assistant."),
            ("human", "{question}"),
        ]
    )

    # The model is intentionally injected by the application rather than
    # hard-coded here. A configured chat model can be composed with this prompt.
    def missing_model(_: dict[str, str]) -> str:
        raise RuntimeError("Configure a chat model before invoking the chain.")

    return prompt | RunnableLambda(missing_model) | StrOutputParser()


@app.post("/generate", response_model=PromptResponse)
def generate(payload: PromptRequest) -> PromptResponse:
    """Expose a LangChain pipeline through a validated FastAPI endpoint."""
    try:
        chain = build_chain()
        result = chain.invoke({"question": payload.question})
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return PromptResponse(answer=str(result))
