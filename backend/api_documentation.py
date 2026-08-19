"""
Day 19 - API Documentation

Topics:
- API documentation
- OpenAPI
- Swagger
- API contracts
- Request/response schemas
- HTTP status codes
"""


OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Task Manager API",
        "description": (
            "API contract for the Task Manager backend."
        ),
        "version": "1.0.0",
    },
    "servers": [
        {
            "url": "http://localhost:5000",
            "description": "Local development server",
        }
    ],
    "paths": {
        "/api/tasks": {
            "get": {
                "summary": "List tasks",
                "description": (
                    "Returns a paginated list of tasks."
                ),
                "parameters": [
                    {
                        "name": "page",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "minimum": 1,
                            "default": 1,
                        },
                    },
                    {
                        "name": "page_size",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "default": 10,
                        },
                    },
                    {
                        "name": "completed",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "boolean",
                        },
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Tasks returned successfully.",
                    },
                    "400": {
                        "description": "Invalid query parameters.",
                    },
                    "401": {
                        "description": "Authentication required.",
                    },
                },
            },
            "post": {
                "summary": "Create task",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/TaskCreate"
                            }
                        }
                    },
                },
                "responses": {
                    "201": {
                        "description": "Task created successfully.",
                    },
                    "400": {
                        "description": "Invalid request body.",
                    },
                    "401": {
                        "description": "Authentication required.",
                    },
                },
            },
        },
        "/api/tasks/{task_id}": {
            "get": {
                "summary": "Get a task",
                "parameters": [
                    {
                        "name": "task_id",
                        "in": "path",
                        "required": True,
                        "schema": {
                            "type": "integer",
                        },
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Task returned successfully.",
                    },
                    "401": {
                        "description": "Authentication required.",
                    },
                    "404": {
                        "description": "Task not found.",
                    },
                },
            }
        },
    },
    "components": {
        "schemas": {
            "TaskCreate": {
                "type": "object",
                "required": ["title"],
                "properties": {
                    "title": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "maxLength": 1000,
                    },
                    "priority": {
                        "type": "string",
                        "enum": [
                            "low",
                            "medium",
                            "high",
                        ],
                        "default": "medium",
                    },
                    "completed": {
                        "type": "boolean",
                        "default": False,
                    },
                },
            },
            "Task": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer",
                    },
                    "title": {
                        "type": "string",
                    },
                    "description": {
                        "type": "string",
                    },
                    "priority": {
                        "type": "string",
                    },
                    "completed": {
                        "type": "boolean",
                    },
                },
            },
        }
    },
}


def get_openapi_spec() -> dict:
    """
    Return the OpenAPI specification.

    Keeping the specification as data makes it possible to expose
    it later through an endpoint or connect it to Swagger UI.
    """
    return OPENAPI_SPEC


def print_api_summary() -> None:
    """Print the documented endpoints."""
    for path, methods in OPENAPI_SPEC["paths"].items():
        for method, definition in methods.items():
            summary = definition.get("summary", "")
            print(f"{method.upper():6} {path:25} {summary}")


if __name__ == "__main__":
    print("Task Manager API - OpenAPI Specification")
    print("=" * 60)
    print_api_summary()