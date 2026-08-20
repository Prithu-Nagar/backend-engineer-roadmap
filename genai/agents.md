# AI Agents

AI agents are systems that use an LLM to reason about a task, select actions, call tools, observe results, and continue until the task is completed or a stopping condition is reached.

---

## LLM Application vs Agent

A simple LLM application:

```text
User
 |
 v
Prompt
 |
 v
LLM
 |
 v
Response
```

An agent:

```text
User
 |
 v
Agent
 |
 v
LLM
 |
 +----> Decide action
 |
 v
Tool
 |
 v
Tool result
 |
 v
LLM
 |
 +----> Continue
 |
 v
Final response
```

The important difference is that an agent can use tools and iteratively decide what to do next.

### Core Components

A basic agent consists of:

- Model
- Prompt/instructions
- Tools
- Tool execution layer
- State
- Agent loop
- Stopping conditions
- Guardrails

## Tool Calling

A tool is a controlled function that an agent can invoke.

Example:

```python
def get_task(task_id: int) -> dict:
    ...
```

The model should not directly execute arbitrary code.

Instead:

```text
LLM
 |
 | Tool request
 v
Application
 |
 | Validate arguments
 v
Tool
 |
 v
Tool result
 |
 v
LLM
```

### Example Tools

A backend agent might have:

- `get_task()`
- `create_task()`
- `search_tasks()`
- `get_user()`
- `calculate_total()`

Each tool should have:

- Name
- Description
- Input schema
- Output format
- Validation rules
- Permission requirements

## Agent Loop

A simplified agent loop:

1. Receive user request
2. Send request to model
3. Model decides whether a tool is required
4. Validate tool call
5. Execute tool
6. Return tool result to model
7. Model evaluates the result
8. Repeat if another action is needed
9. Return final response

### Pseudocode

```python
while not finished:
    response = model(messages, tools)

    if response.is_final:
        return response.content

    tool_call = response.tool_call

    validate_tool_call(tool_call)

    result = execute_tool(tool_call)

    messages.append(tool_call)
    messages.append(result)
```

## Tool Validation

Never blindly trust model-generated tool arguments.

Validate:

- Tool name
- Input types
- Required fields
- Allowed values
- Authorization
- Resource ownership
- Rate limits

For example:

```python
if not isinstance(task_id, int):
    raise ValueError("task_id must be an integer")
```

The model decides what it wants to do.

The application decides whether it is allowed to do it.

## Agent State

Agents may need state containing:

- User request
- Previous model messages
- Tool calls
- Tool results
- Intermediate reasoning state
- Task progress
- Limits and counters

State can be:

- In-memory
- Database-backed
- Redis-backed
- Workflow-engine backed

## Stopping Conditions

An agent should not run forever.

Possible stopping conditions:

- Final answer produced
- Maximum iterations reached
- Tool failure
- Timeout
- Budget exceeded
- Invalid tool call
- Safety/authorization rejection

Example:

```python
MAX_ITERATIONS = 10

for _ in range(MAX_ITERATIONS):
    ...
```

## Guardrails

Agents need boundaries around:

- Tool access
- Data access
- User permissions
- Sensitive operations
- Rate limits
- Token budgets
- Execution time

A useful architecture is:

```text
User
 |
 v
Agent
 |
 v
Policy / Guardrail Layer
 |
 v
Tool Validation
 |
 v
Tool Execution
```
