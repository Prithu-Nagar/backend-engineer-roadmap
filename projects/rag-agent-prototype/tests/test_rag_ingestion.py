from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from rag_agent import DocumentChunk, LexicalRetriever, build_demo_agent
from rag_ingestion import (
    DocumentChunker,
    DocumentIngestionPipeline,
    HashingEmbeddingProvider,
    InMemoryVectorStore,
    OpenAIEmbeddingProvider,
    SourceDocument,
    VectorRetriever,
    load_text_file,
)


def test_chunker_preserves_document_metadata_and_indexes_chunks():
    chunker = DocumentChunker(chunk_size=12, overlap=3)
    chunks = chunker.split(SourceDocument("doc-1", "alpha beta gamma delta", {"source": "guide.md"}))
    assert len(chunks) > 1
    assert chunks[0].document_id == "doc-1"
    assert chunks[0].metadata["source"] == "guide.md"
    assert chunks[0].metadata["chunk_index"] == "0"
    assert all("start_char" in chunk.metadata and "end_char" in chunk.metadata for chunk in chunks)


def test_text_file_loader_reads_content_and_source_metadata(tmp_path):
    source = tmp_path / "handbook.md"
    source.write_text("RAG ingestion source", encoding="utf-8")
    document = load_text_file(source, metadata={"team": "platform"})
    assert document.document_id == "handbook"
    assert document.text == "RAG ingestion source"
    assert document.metadata["source"] == str(source)
    assert document.metadata["team"] == "platform"


def test_chunker_returns_no_chunks_for_blank_document():
    assert DocumentChunker().split(SourceDocument("empty", "  \n ")) == []


def test_chunker_validates_size_and_overlap():
    with pytest.raises(ValueError):
        DocumentChunker(chunk_size=0)
    with pytest.raises(ValueError):
        DocumentChunker(chunk_size=10, overlap=10)


def test_hashing_embedder_is_deterministic_and_normalized():
    embedder = HashingEmbeddingProvider()
    first = embedder.embed_query("vector retrieval")
    assert first == embedder.embed_query("vector retrieval")
    assert sum(value * value for value in first) == pytest.approx(1.0)


def test_ingestion_pipeline_chunks_embeds_and_indexes_documents():
    store = InMemoryVectorStore()
    pipeline = DocumentIngestionPipeline(DocumentChunker(20, 4), HashingEmbeddingProvider(), store)
    chunks = pipeline.ingest([SourceDocument("guide", "RAG uses retrieval and embeddings.", {"kind": "guide"})])
    assert chunks
    assert len(store) == len(chunks)
    assert chunks[0].metadata["kind"] == "guide"


def test_ingestion_pipeline_skips_embedding_for_empty_input():
    store = InMemoryVectorStore()
    pipeline = DocumentIngestionPipeline(DocumentChunker(), HashingEmbeddingProvider(), store)
    assert pipeline.ingest([SourceDocument("empty", "")]) == []
    assert len(store) == 0


def test_vector_retriever_returns_ranked_results():
    store = InMemoryVectorStore()
    embedder = HashingEmbeddingProvider()
    chunks = [
        DocumentChunk("rag", "RAG retrieval uses vector embeddings"),
        DocumentChunk("billing", "Invoices and payment reconciliation"),
    ]
    store.add(chunks, embedder.embed_documents([chunk.text for chunk in chunks]))
    results = VectorRetriever(embedder, store).search("vector embeddings retrieval")
    assert results
    assert results[0].chunk.document_id == "rag"
    assert results[0].score <= 1.0


def test_vector_store_validates_embedding_counts_and_dimensions():
    store = InMemoryVectorStore()
    with pytest.raises(ValueError):
        store.add([DocumentChunk("a", "text")], [])
    store.add([DocumentChunk("a", "text")], [[1.0, 0.0]])
    with pytest.raises(ValueError):
        store.add([DocumentChunk("b", "text")], [[1.0]])
    with pytest.raises(ValueError):
        store.search([1.0])


def test_vector_store_and_retriever_validate_top_k_and_blank_query():
    store = InMemoryVectorStore()
    with pytest.raises(ValueError):
        store.search([1.0], top_k=0)
    assert VectorRetriever(HashingEmbeddingProvider(), store).search("  ") == []


def test_openai_embedding_adapter_parses_provider_response(monkeypatch):
    def fake_urlopen(request, timeout):
        payload = json.loads(request.data.decode())
        data = [
            {"index": index, "embedding": [1.0, 0.0] if index == 0 else [0.0, 1.0]}
            for index, _ in enumerate(payload["input"])
        ]
        response = MagicMock()
        response.__enter__.return_value.read.return_value = json.dumps({"data": data}).encode()
        return response

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    provider = OpenAIEmbeddingProvider(api_key="test-key")
    assert provider.embed_documents(["first", "second"]) == [[1.0, 0.0], [0.0, 1.0]]
    assert provider.embed_query("query") == [1.0, 0.0]


def test_openai_embedding_adapter_requires_credentials(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        OpenAIEmbeddingProvider(api_key="")


def test_existing_lexical_retriever_and_agent_remain_compatible():
    lexical = LexicalRetriever([DocumentChunk("existing", "RAG retrieval context")])
    assert lexical.search("RAG")
    output = build_demo_agent().run("How should RAG retrieval be separated from answer generation?")
    assert "Retrieved context:" in output
    assert "rag-retrieval" in output
    assert "Tool result:" in build_demo_agent().run("status retrieval-service")
