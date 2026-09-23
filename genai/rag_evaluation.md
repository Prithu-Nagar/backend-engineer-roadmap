# RAG Evaluation

Day 54 focuses on making RAG evaluation reproducible through explicit metrics,
versioned test sets, and separate retrieval and answer-quality analysis.

RAG systems should be evaluated across both retrieval and generation.

---

## Retrieval Evaluation

Important retrieval metrics include:

- Precision
- Recall
- `Precision@K`
- `Recall@K`
- Mean Reciprocal Rank (MRR)
- NDCG

### Precision

Measures how many of the retrieved results are relevant.

```text
            Relevant Retrieved Results
Precision = --------------------------
            Total Retrieved Results
```

### Recall

Measures how much of the relevant information was retrieved.

```text
         Relevant Retrieved Results
Recall = --------------------------
         Total Relevant Results
```

### Precision@K

Measures the proportion of relevant results among the top `K` retrieved results.

```text
               Relevant Results in Top K
Precision@K = --------------------------
                          K
```

### Recall@K

Measures the proportion of all relevant results that were retrieved within the top `K` results.

```text
            Relevant Results in Top K
Recall@K = --------------------------
            Total Relevant Results
```

### Mean Reciprocal Rank (MRR)

Measures how highly the first relevant result appears in the ranked retrieval results.

```text
MRR = Average of (1 / Rank of First Relevant Result)
```

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

```text
Question
   ↓
Expected Answer
   ↓
Expected Source
```

The same evaluation dataset can be run against different versions of the RAG pipeline.

---

## Retrieval vs. Generation Failures

When a RAG answer is incorrect, determine which stage caused the problem.

```text
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
```

### Retrieval Failure

The required information was not retrieved or the wrong documents were retrieved.

### Generation Failure

The correct information was retrieved, but the model produced an incorrect, incomplete, or unsupported answer.

These failures should be diagnosed separately.

---

## RAG Evaluation Dimensions

| Stage | Evaluation |
| --- | --- |
| Retrieval | Precision, Recall, `Precision@K`, `Recall@K`, MRR, NDCG |
| Context | Relevance and completeness |
| Generation | Faithfulness, relevance, correctness |
| System | Latency, cost, and reliability |

---

## Key Takeaway

A RAG system should not be evaluated only by whether the final answer appears correct.

Evaluation should cover:

```text
Retrieval Quality
        +
Context Quality
        +
Generation Quality
        +
System Performance
```

---

## Day 54 — Evaluation Workflow

A repeatable evaluation run should keep the dataset and pipeline version
explicit.

```text
Versioned Test Set
        |
        v
   RAG Pipeline
        |
        +---- Retrieval Metrics
        |
        +---- Context Metrics
        |
        +---- Answer Metrics
        |
        +---- Latency / Cost
        |
        v
   Evaluation Run
```

### Retrieval Metrics

Use retrieval metrics to answer whether the relevant evidence was found:

- `Precision@K` — fraction of the top-K results that are relevant.
- `Recall@K` — fraction of known relevant results recovered in the top K.
- `MRR` — rewards placing the first relevant result near the top.
- `NDCG` — evaluates ranked relevance when relevance can have graded values.

Metrics should be interpreted against a fixed test set and retrieval policy;
changing the dataset can change the apparent score without changing the
pipeline.

### Answer Quality

Evaluate the generated response separately from retrieval:

- **Faithfulness:** Is the answer supported by the retrieved context?
- **Answer relevance:** Does the response address the user's question?
- **Correctness:** Does it agree with trusted expected information?
- **Citation/source coverage:** Are important claims traceable to retrieved sources?

### Test-Set Design

A useful RAG test set should contain:

- Representative user questions
- Expected answers or grading guidance
- Relevant document/chunk identifiers
- Dataset name and version
- Optional metadata for tenant, product, language, or difficulty

Keep evaluation cases stable so changes to retrieval, chunking, prompts, or
models can be compared fairly.

### Regression Testing

Run the same test set against each pipeline version and compare:

| Area | Example signal |
| --- | --- |
| Retrieval | Recall@K, MRR, NDCG |
| Context | Relevance, completeness |
| Generation | Faithfulness, relevance, correctness |
| Operations | Latency, errors, token usage, cost |

A regression should be investigated by locating the failing stage instead of
assuming the LLM is responsible.

### Retrieval Failure vs Generation Failure

```text
Question
   |
   v
Retrieval ----X----> Required evidence missing
   |
   v
Context
   |
   v
Generation ----X----> Evidence present but answer unsupported
```

This separation makes debugging and targeted improvements more practical.
