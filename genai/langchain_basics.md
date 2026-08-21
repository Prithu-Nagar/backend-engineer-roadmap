# LangChain Fundamentals

## Overview

LangChain is a framework for building applications that work with language models.

Day 13 focuses on the fundamental building blocks:

- Models
- Prompts
- Chains
- Prompt templates
- Basic composition

---

## Models

A model is responsible for processing input and generating an output.

Conceptually:

```text
Input
  ↓
Model
  ↓
Output
```

Models can be used for:

- Text generation
- Summarization
- Classification
- Question answering
- Information extraction

---

## Prompts

A prompt provides instructions and input to the model.

Example:

```text
Explain {topic} for a backend developer.
```

The `{topic}` value can be supplied dynamically.

---

## Prompt Templates

Prompt templates allow the same prompt structure to be reused with different inputs.

Example:

```text
Template:
Explain {topic} for a backend developer.

Input:
topic = "rate limiting"

Result:
Explain rate limiting for a backend developer.
```

Benefits:

- Reusability
- Consistency
- Easier maintenance
- Separation of instructions and input data

---

## Chains

A chain connects multiple processing steps.

### Basic Workflow

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Output
```

A more complex workflow can contain several steps:

```text
Input
  ↓
Prompt
  ↓
Model
  ↓
Parser
  ↓
Application Logic
  ↓
Final Output
```

Chains make multi-step workflows easier to organize and compose.

---

## Basic Composition

A LangChain-style application can separate responsibilities:

```text
Application
    ↓
Prompt
    ↓
Model
    ↓
Output Processing
    ↓
Application Response
```

This separation makes model interaction easier to maintain and test.

---

## Backend Integration

LangChain can be used as part of a Python backend application.

Conceptually:

```text
Client
  ↓
Backend API
  ↓
Application Logic
  ↓
LangChain
  ↓
Model Provider
  ↓
Response
```

The backend remains responsible for concerns such as:

- Authentication
- Validation
- Business logic
- API responses
- Error handling

LangChain handles the model-oriented workflow.

---

## Key Takeaways

### Model

Processes input and generates output.

### Prompt

Provides instructions and input to the model.

### Prompt Template

Provides a reusable prompt structure with variables.

### Chain

Connects multiple processing steps into a workflow.

The fundamental relationship is:

```text
Prompt + Model → Output
```

and:

```text
Input → Prompt → Model → Output
```

These fundamentals provide the base for later topics such as RAG, tool integration, and agents.
