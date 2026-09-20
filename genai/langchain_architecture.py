"""
Day 51 — LangChain Architecture

A minimal provider-neutral LangChain pipeline showing separation between
prompt construction, model invocation, and output parsing.

The model is injected into the builder so credentials and provider-specific
configuration remain outside the reusable workflow.
"""

from typing import Any


def build_chain(model: Any) -> Any:
    """Build Prompt -> Model -> String Parser."""
    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as exc:
        raise RuntimeError(
            "Install langchain-core to run this example."
        ) from exc

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a concise backend engineering assistant.",
            ),
            ("human", "{question}"),
        ]
    )

    return prompt | model | StrOutputParser()


def invoke_chain(chain: Any, question: str) -> str:
    """Invoke a configured chain with validated input."""
    if not question.strip():
        raise ValueError("question must not be empty")

    result = chain.invoke({"question": question})
    return str(result)
