# Vector Databases

Vector databases are designed to store, index, and search vector embeddings efficiently.

They are commonly used for:

- Semantic search
- Similarity search
- Retrieval-Augmented Generation (RAG)
- Recommendation systems
- Document retrieval

---

## Embeddings

An embedding is a numerical representation of data such as text or documents.

```text
Text
  ↓
Embedding Model
  ↓
Vector
[0.12, -0.45, 0.78, ...]
```

The embedding captures semantic information that can be used for similarity-based retrieval.

---

## Vector Search

Instead of searching for exact keywords, vector search finds information that is semantically similar to a query.

```text
User Query
    ↓
Embedding Model
    ↓
Query Vector
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Relevant Results
```

For example, a query about:

"Python API development"

can retrieve documents discussing Flask or REST APIs even when the exact words are different.

---

## Similarity Metrics

Common metrics include:

- Cosine similarity
- Euclidean distance
- Dot product

### Cosine Similarity

Measures the angle between two vectors.

cos(θ) = (A · B) / (||A|| ||B||)

Higher similarity generally indicates that the vectors are closer in direction.

---

## Approximate Nearest Neighbor Search

Comparing a query against every stored vector becomes expensive as the dataset grows.

Approximate Nearest Neighbor (ANN) techniques improve search performance.

Common approaches include:

- HNSW
- IVF
- Product Quantization

---

## HNSW

HNSW (Hierarchical Navigable Small World) is a graph-based ANN indexing technique.

Conceptually:

```text
Query
  ↓
Upper-level graph
  ↓
Narrow search
  ↓
Lower-level graph
  ↓
Nearest vectors
```

It allows efficient navigation through a vector graph instead of exhaustively scanning every vector.

---

## Metadata

Vectors are commonly stored with metadata.

```json
{
    "document_id": 101,
    "category": "backend",
    "language": "python"
}
```

Metadata can be used to filter search results.

Example:

```text
Semantic Search
      +
category = "backend"
      ↓
Filtered Results
```

---

## Top-K Retrieval

Vector searches commonly return the top `K` most similar results.

K = 5

Result 1
Result 2
Result 3
Result 4
Result 5

Choosing `K` involves a trade-off:

- Too few results → potentially missing relevant information
- Too many results → potentially introducing irrelevant context

---

## Vector Databases and RAG

Vector databases are commonly used as the retrieval layer in RAG systems.

```text
Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Answer
```

The vector database retrieves relevant information that can be provided to the language model as context.

---

## Vector Database vs Traditional Database

| Feature        | Traditional Database | Vector Database       |
| -------------- | -------------------- | --------------------- |
| Primary search | Structured / exact   | Similarity            |
| Typical data   | Structured records   | Embeddings + metadata |
| Query style    | SQL                  | Vector search         |
| Common use     | Transactions         | Semantic retrieval    |

They can also work together:

```text
Application
    ├── PostgreSQL → Structured data
    └── Vector DB  → Semantic retrieval
```

---

## Vector Database vs Vector Index

A vector index is a data structure used to make similarity searches faster.

A vector database provides a broader system for:

- Vector storage
- Indexing
- Metadata
- Search
- APIs
- Persistence

---

## Common Technologies

Examples include:

- Pinecone
- ChromaDB
- Weaviate
- FAISS

FAISS is primarily a similarity-search library rather than a complete managed vector database.

---

## Use Cases

Vector databases are useful for:

- Semantic document search
- RAG applications
- Recommendation systems
- Similarity matching
- Natural-language search

---

## Task Manager Application

A vector database is not required for the current Task Manager CRUD API.

It could become useful later for features such as:

- Semantic task search
- Natural-language task queries
- AI-powered task recommendations

Example:

"Find tasks related to backend performance"
```text
                ↓
            Embedding
                ↓
          Vector Search
                ↓
          Relevant Tasks
```

This would be a future extension rather than part of the current CRUD implementation.

---

## Key Takeaways

```text
Embeddings
    ↓
Vector Database
    ↓
Similarity Search
    ↓
Relevant Results
```

For RAG:

```text
Documents
    ↓
Embeddings
    ↓
Vector Database
    ↓
Retrieval
    ↓
Context
    ↓
LLM
    ↓
Answer
```

**Core idea:** Vector databases enable efficient similarity-based retrieval of information represented as embeddings.
