"""Provider-neutral RAG + tool-using agent prototype.

The implementation is deterministic and intentionally keeps retrieval, tools,
and orchestration behind small application-owned interfaces.
"""

import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class DocumentChunk:
    document_id: str
    text: str
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalResult:
    chunk: DocumentChunk
    score: float


class LexicalRetriever:
    """Small deterministic retriever used in place of a vector database."""

    def __init__(self, chunks: Sequence[DocumentChunk]) -> None:
        self._chunks = list(chunks)

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]+", text.lower()))

    def search(self, query: str, top_k: int = 3) -> list[RetrievalResult]:
        query_tokens = self._tokens(query)
        scored = []
        for chunk in self._chunks:
            score = len(query_tokens & self._tokens(chunk.text))
            if score:
                scored.append(RetrievalResult(chunk=chunk, score=score))
        scored.sort(key=lambda result: (-result.score, result.chunk.document_id))
        return scored[:top_k]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[[dict[str, str]], str]
    required_argument: str


class ToolRegistry:
    """Application-owned allow-list for agent tools."""

    def __init__(self, tools: Sequence[Tool], max_argument_length: int = 256) -> None:
        if max_argument_length <= 0:
            raise ValueError("max_argument_length must be positive")
        self.max_argument_length = max_argument_length
        self._tools: dict[str, Tool] = {}
        for tool in tools:
            if not tool.name or tool.name in self._tools:
                raise ValueError("Tool names must be non-empty and unique")
            self._tools[tool.name] = tool

    def execute(self, name: str, arguments: dict[str, str]) -> str:
        tool = self._tools.get(name)
        if tool is None:
            raise ValueError(f"Tool is not allowed: {name}")
        value = arguments.get(tool.required_argument)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Missing or empty required argument: {tool.required_argument}")
        if len(value) > self.max_argument_length:
            raise ValueError(f"Tool argument exceeds {self.max_argument_length} characters")
        return tool.handler({tool.required_argument: value.strip()})


class RagAgent:
    """Simple routing layer that chooses retrieval or an approved tool."""

    def __init__(
        self, retriever: LexicalRetriever, tools: ToolRegistry, max_query_chars: int = 2000
    ) -> None:
        if max_query_chars <= 0:
            raise ValueError("max_query_chars must be positive")
        self.retriever = retriever
        self.tools = tools
        self.max_query_chars = max_query_chars

    def run(self, query: str) -> str:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must not be empty")
        if len(query) > self.max_query_chars:
            raise ValueError(f"query exceeds {self.max_query_chars} characters")
        normalized = query.lower()
        if normalized.startswith("status "):
            service = query[7:].strip()
            result = self.tools.execute("service_status", {"service": service})
            return f"Tool result: {result}"

        results = self.retriever.search(query)
        if not results:
            return "No relevant context was retrieved."

        context = "\n".join(
            f"[{result.chunk.document_id}] {result.chunk.text}"
            for result in results
        )
        return (
            "Retrieved context:\n"
            f"{context}\n\n"
            "Answer boundary: use only the retrieved context for the next model step."
        )


def build_demo_agent() -> RagAgent:
    chunks = [
        DocumentChunk(
            "backend-rate-limits",
            "AI endpoints should use tenant-aware rate limits and token budgets to control cost.",
        ),
        DocumentChunk(
            "rag-retrieval",
            "RAG separates document ingestion, chunking, retrieval, context assembly, and answer generation.",
        ),
        DocumentChunk(
            "ai-reliability",
            "AI services should use bounded retries, timeouts, fallbacks, and stable client-facing errors.",
        ),
    ]

    def service_status(args: dict[str, str]) -> str:
        service = args["service"]
        return f"{service}: healthy (demo response)"

    tools = ToolRegistry(
        [
            Tool(
                name="service_status",
                description="Return the demo health state of a named service.",
                handler=service_status,
                required_argument="service",
            )
        ]
    )
    return RagAgent(LexicalRetriever(chunks), tools)


if __name__ == "__main__":
    agent = build_demo_agent()
    print(agent.run("How should RAG retrieval be separated from answer generation?"))
    print(agent.run("status retrieval-service"))
