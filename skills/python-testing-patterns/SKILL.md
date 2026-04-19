---
name: python-testing-patterns
description: Comprehensive testing strategies in Python using Pytest, fixtures, mocking, and TDD methodology.
category: Python
license: Private
---

# Python Testing Patterns

## When to use this skill

Apply this skill when you:
- Construct robust testing suites for Python applications.
- Need to isolate external systems (APIs, Databases, S3) using `unittest.mock`.
- Manage reusable test data with Pytest fixtures.
- Embrace Test-Driven Development (TDD) for building deterministic code.

## Pytest Fixtures

`pytest` outshines `unittest` by providing composable and decoupled `fixtures` for dependency injection.

```python
import pytest

@pytest.fixture
def database_connection():
    # Setup
    conn = Database.connect(":memory:")
    yield conn
    # Teardown
    conn.disconnect()

def test_user_creation(database_connection):
    user = User(name="Alice")
    database_connection.save(user)
    assert database_connection.count() == 1
```

## Mocking External Dependencies

Calls overlapping the network boundaries must be mocked ensuring fast and repeatable tests.

```python
from unittest.mock import patch

def test_fetch_external_data():
    with patch("myapp.services.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"id": 1, "name": "Fake"}
        
        result = myapp.services.fetch_user()
        assert result["name"] == "Fake"
        mock_get.assert_called_once()
```

## Test-Driven Development (TDD) Guidelines

1. **Red**: Write a minimal failing test addressing the behavior you intend to resolve.
2. **Green**: Write the bare minimum piece of code required to pass the test. No premature scaling.
3. **Refactor**: Clean layout, abstract shared fixtures, remove unneeded loops while ensuring the test keeps passing.

## Advanced Patterns

### Parametrize

Use `pytest.mark.parametrize` to avoid duplicating tests meant to assert the exact same function over diverse input parameters.

```python
@pytest.mark.parametrize("input_data, expected", [
    ("", False),
    ("valid@email.com", True),
    ("invalid_email", False),
])
def test_email_validation(input_data, expected):
    assert is_valid_email(input_data) is expected
```
