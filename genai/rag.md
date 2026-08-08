# Retrieval-Augmented Generation

Retrieval-Augmented Generation (RAG) combines information retrieval with language generation.

## Architecture

Documents
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
    ↓
User Query
    ↓
Similarity Search
    ↓
Relevant Context
    ↓
LLM
    ↓
Answer

## Indexing

Documents are split into chunks and converted into embeddings.

Document
   ↓
Chunks
   ↓
Embeddings
   ↓
Vector Database

## Retrieval

The user query is converted into an embedding and compared against stored vectors.

Query
  ↓
Embedding
  ↓
Similarity Search
  ↓
Top-K Results

## Generation

Retrieved information is provided to the LLM as context.

Question + Retrieved Context
              ↓
             LLM
              ↓
            Answer

## RAG vs Fine-Tuning

| RAG                                    | Fine-Tuning                     |
| -------------------------------------- | ------------------------------- |
| Retrieves external information         | Changes model behavior          |
| Knowledge can be updated externally    | Requires model training         |
| Useful for document-based applications | Useful for specialized behavior |

## Production Considerations

* Chunking strategy
* Embedding model
* Retrieval quality
* Top-K selection
* Metadata filtering
* Context size
* Evaluation
