"""Run the RAG prototype locally or with live OpenAI providers."""

from __future__ import annotations

import argparse

from rag_generation import GroundedAnswerGenerator, OpenAIChatCompletionProvider
from rag_ingestion import (
    DocumentChunker,
    DocumentIngestionPipeline,
    HashingEmbeddingProvider,
    InMemoryVectorStore,
    OpenAIEmbeddingProvider,
    SourceDocument,
    VectorRetriever,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use live OpenAI embedding and answer-generation APIs (requires OPENAI_API_KEY).",
    )
    parser.add_argument("--question", default="What does a RAG pipeline separate?")
    args = parser.parse_args()

    documents = [
        SourceDocument(
            "rag-overview",
            "A RAG pipeline separates document ingestion, chunking, retrieval, context assembly, and answer generation.",
            {"source": "inline-demo"},
        ),
        SourceDocument(
            "reliability",
            "AI services should use bounded retries, timeouts, fallbacks, and stable client-facing errors.",
            {"source": "inline-demo"},
        ),
    ]
    if args.live:
        embedder = OpenAIEmbeddingProvider()
    else:
        embedder = HashingEmbeddingProvider()

    store = InMemoryVectorStore()
    DocumentIngestionPipeline(DocumentChunker(), embedder, store).ingest(documents)
    results = VectorRetriever(embedder, store).search(args.question)

    if not results:
        print("No relevant source was retrieved.")
        return

    if not args.live:
        print("Offline retrieval demo (feature hashing; not semantic embeddings).")
        for result in results:
            print(f"[source:{result.chunk.document_id}] {result.chunk.text}")
        print("Run with --live to generate an answer using the configured provider.")
        return

    answer = GroundedAnswerGenerator(OpenAIChatCompletionProvider()).generate(
        args.question, results
    )
    print(answer.answer)
    print("Sources:", ", ".join(answer.source_ids) if answer.source_ids else "none")
    print("Abstained:", answer.abstained)


if __name__ == "__main__":
    main()
