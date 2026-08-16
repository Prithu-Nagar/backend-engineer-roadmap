"""
Day 16 - LangChain Retrievers and Prompt Pipelines

This file demonstrates the conceptual structure of a retrieval
and prompt pipeline without requiring external model credentials.
"""


def simple_retriever(query, documents, top_k=2):
    """
    Very small keyword-based retriever for demonstration.

    This is NOT a production vector retriever.
    It is only used to demonstrate the retrieval concept.
    """
    query_words = set(query.lower().split())

    scored_documents = []

    for document in documents:
        words = set(document.lower().split())
        score = len(query_words & words)

        scored_documents.append((score, document))

    scored_documents.sort(reverse=True)

    return [
        document
        for score, document in scored_documents[:top_k]
        if score > 0
    ]


def build_prompt(question, context):
    """Build a simple retrieval-augmented prompt."""
    context_text = "\n".join(context)

    return f"""
Use the following context to answer the question.

Context:
{context_text}

Question:
{question}

Answer:
""".strip()


def retrieval_pipeline(question, documents):
    """Run retrieval followed by prompt construction."""
    context = simple_retriever(question, documents)

    prompt = build_prompt(question, context)

    return {
        "question": question,
        "context": context,
        "prompt": prompt,
    }


if __name__ == "__main__":
    documents = [
        "Redis is an in-memory data store.",
        "Python generators provide lazy evaluation.",
        "API validation protects backend services from invalid input.",
        "LangChain can be used to compose LLM application pipelines.",
    ]

    result = retrieval_pipeline(
        "How does API validation protect backend services?",
        documents,
    )

    print("Retrieved context:")
    for document in result["context"]:
        print("-", document)

    print("\nPrompt:")
    print(result["prompt"])