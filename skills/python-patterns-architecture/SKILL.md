---
name: python-patterns-architecture
description: Advanced software development principles, type hints, clean architecture, and maintainable structure in Python.
category: Python
license: Private
---

# Python Architecture & Patterns

## When to use this skill

Activate this protocol when you:
- Need to refactor a large monolithic Python codebase into a clean architecture.
- Are defining domain models and need strict type definitions using `typing` or `pydantic`.
- Face complexity managing dependencies, applying Inversion of Control (IoC), and dependency injection in Python.

## Type Hints and Strict Checking

Modern Python relies heavily on Type Hints for developer experience and CI validation.

```python
from typing import List, Optional, Callable
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    email: Optional[str] = None

def get_active_users(users: List[User], is_active: Callable[[User], bool]) -> List[User]:
    return [u for u in users if is_active(u)]
```

Always use tools like `mypy` or `pyright` in strict mode to ensure type safety across the domain layer.

## The Clean Architecture in Python

Separate your system into distinct layers indicating the dependency rule: Inner layers (entities) know nothing about outer layers (frameworks / databases).

### 1. Domain / Entities
Pure Python classes (`dataclasses` or standard classes). No knowledge of SQLAlchemy, Django, or FastAPI.

### 2. Use Cases (Application Business Rules)
Orchestrate the flow of data using Domain objects.

### 3. Adapters (Interfaces)
Repositories and controllers. Translate data between the use cases and external agencies.

```python
from abc import ABC, abstractmethod

# The Interface (Adapter Layer mapping)
class UserRepositoryLayer(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

# The Use Case requiring it
class BlockUserUseCase:
    def __init__(self, repo: UserRepositoryLayer):
        self.repo = repo

    def execute(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        # Apply business rule logic
        return user
```

### 4. Frameworks & Drivers
The outermost layer (Web API, DB connection). Construct dependencies here and pass them down (Dependency Injection).

## Standardized Error Handling

Do not scatter raw exceptions. Define custom domain-level exceptions and map them to appropriate HTTP/gRPC responses at the adapter boundary.
