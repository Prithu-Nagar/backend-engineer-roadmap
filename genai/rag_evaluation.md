# RAG Evaluation

RAG systems should be evaluated across both retrieval and generation.

---

## Retrieval Evaluation

Important retrieval metrics include:

- Precision
- Recall
- Precision@K
- Recall@K
- Mean Reciprocal Rank (MRR)
- NDCG

### Precision

Measures how many of the retrieved results are relevant.

Precision =
Relevant Retrieved Results
--------------------------
Total Retrieved Results

### Recall

Measures how much of the relevant information was retrieved.

Recall =
Relevant Retrieved Results
--------------------------
Total Relevant Results

### Precision@K

Measures the proportion of relevant results among the top K retrieved results.

Precision@K =
Relevant Results in Top K
-------------------------
K

### Recall@K

Measures the proportion of all relevant results that were retrieved within the top K results.

Recall@K =
Relevant Results in Top K
-------------------------
Total Relevant Results

### Mean Reciprocal Rank (MRR)

Measures how highly the first relevant result appears in the ranked retrieval results.

MRR =
Average of 1 / Rank of First Relevant Result

### NDCG

Normalized Discounted Cumulative Gain evaluates the quality of ranked results while giving greater importance to relevant results appearing near the top.

---

## Generation Evaluation

Retrieval quality alone does not guarantee a good final answer.

The generated response should also be evaluated.

### Faithfulness

Measures whether the generated answer is supported by the retrieved context.

### Answer Relevance

Measures whether the generated answer directly addresses the user's question.

### Correctness

Measures whether the generated answer matches trusted or expected information.

---

## Evaluation Dataset

A RAG system should have a representative evaluation dataset containing questions and expected answers and/or relevant source documents.

The dataset can be used for:

- Regression testing
- Comparing retrieval strategies
- Evaluating prompt changes
- Measuring system improvements
- Detecting quality regressions

Example:

Question
   ↓
Expected Answer
   ↓
Expected Source

The same evaluation dataset can be run against different versions of the RAG pipeline.

---

## Retrieval vs Generation Failures

When a RAG answer is incorrect, determine which stage caused the problem.

Question
   ↓
Query Processing
   ↓
Retrieval
   ↓
Context Construction
   ↓
Generation
   ↓
Final Answer

### Retrieval Failure

The required information was not retrieved or the wrong documents were retrieved.

### Generation Failure

The correct information was retrieved, but the model produced an incorrect, incomplete, or unsupported answer.

These failures should be diagnosed separately.

---

## RAG Evaluation Dimensions

A practical RAG evaluation should consider:

| Stage      | Evaluation                                          |
| ---------- | --------------------------------------------------- |
| Retrieval  | Precision, Recall, Precision@K, Recall@K, MRR, NDCG |
| Context    | Relevance and completeness                          |
| Generation | Faithfulness, relevance, correctness                |
| System     | Latency, cost, and reliability                      |

---

## Key Takeaway

A RAG system should not be evaluated only by whether the final answer appears correct.

Evaluation should cover:

Retrieval Quality
        +
Context Quality
        +
Generation Quality
        +
System Performance
