# Embeddings

Embeddings are dense numerical vector representations of data such as words, sentences, documents, images, or audio that capture their semantic meaning.

They enable AI models to understand similarity and relationships between different pieces of information.

---

## Why are Embeddings Important?

Computers process numbers, not natural language.

Embeddings convert human-readable data into vectors while preserving semantic relationships.

This enables:

- Semantic Search
- Recommendation Systems
- Retrieval-Augmented Generation (RAG)
- Question Answering
- Clustering
- Classification

---

## Traditional Representation vs Embeddings

### One-Hot Encoding

```text
Cat → [1,0,0]

Dog → [0,1,0]

Car → [0,0,1]
```

Problems:

- Sparse vectors
- Large dimensions
- No semantic meaning

---

### Embeddings

```text
Cat → [0.32, -0.11, 0.74, ...]

Dog → [0.30, -0.08, 0.79, ...]

Car → [-0.91, 0.62, -0.14, ...]
```

Semantically similar concepts are positioned close together in vector space.

---

## Embedding Pipeline

```text
Input Text

↓

Tokenization

↓

Token IDs

↓

Embedding Model

↓

Vector Representation

↓

LLM / RAG / Search / Recommendation System
```

---

## Types of Embeddings

- Word Embeddings
- Sentence Embeddings
- Document Embeddings
- Image Embeddings
- Multimodal Embeddings

---

## Similarity Search

The most common similarity metric is **Cosine Similarity**.

```text
Cosine Similarity =

(A · B)

──────────────

||A|| × ||B||
```

Values:

- 1 → Highly similar
- 0 → Unrelated
- -1 → Opposite

---

## Popular Embedding Models

- Word2Vec
- GloVe
- FastText
- OpenAI Embedding Models
- Gemini Embeddings
- BGE
- E5

---

## Embeddings in RAG

```text
User Query

↓

Embedding Model

↓

Vector

↓

Vector Database

↓

Most Similar Documents

↓

LLM

↓

Final Response
```

Instead of keyword matching, RAG retrieves information using semantic similarity.

---

## Applications

- Semantic Search
- AI Chatbots
- Recommendation Systems
- Fraud Detection
- Duplicate Detection
- Enterprise Search
- Document Retrieval
- Knowledge Bases

---

## Interview Questions

- What are embeddings?
- Why are embeddings required in LLMs?
- Difference between embeddings and one-hot encoding?
- What is cosine similarity?
- Why are embeddings important in RAG?
- What is a vector database?

---

## Summary

- Embeddings convert data into dense numerical vectors.
- Similar concepts are located close together in vector space.
- Cosine Similarity measures semantic similarity.
- Embeddings are a core component of modern LLMs and Retrieval-Augmented Generation systems.