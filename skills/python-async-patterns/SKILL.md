---
name: python-async-patterns
description: Guidelines for asynchronous programming in Python with Asyncio, concurrency handling, and avoiding blocking patterns.
category: Python
license: Private
---

# Async Patterns in Python

## When to use this skill

Routinely adhere to these patterns when you:
- Construct Fast APIs handling vast amounts of concurrent connections.
- Orchestrate networking requests (HTTP calls, crawling, WebSockets).
- Work deeply with database driver I/O bounding (asyncpg, motor).
- Bridge synchronous domains safely to the asynchronous realm.

## The Event Loop Core

`asyncio` implements cooperative multitasking. Instead of the OS handling threads, the code yields execution back to an Event Loop upon encountering IO-Wait blocks by using `await`.

Rule #1: **Never execute a lengthy computation or synchronous sleep in an async def function.** It freezes the entire execution universe.

```python
import asyncio
import time

# WRONG - Freezes every other async task.
async def bad_pattern():
    time.sleep(5)  # The loop stops matching other tasks here.

# RIGHT
async def good_pattern():
    await asyncio.sleep(5)
```

## Running Concurrent Work

Instead of resolving queries one by one, leverage `asyncio.gather` matching independent tasks concurrently.

```python
import asyncio

async def fetch_item(id: int):
    # Simulate DB lookup
    await asyncio.sleep(1)
    return f"Item {id}"

async def main():
    # Will take 1 second in total, not 3 seconds.
    results = await asyncio.gather(
        fetch_item(1),
        fetch_item(2),
        fetch_item(3)
    )
    print(results)
```

## Bridging Sync and Async Environments

If you *inevitably* need to invoke blocking routines (legacy libraries, cryptography hashing, requests module) offload them natively to worker threads without disrupting your Event Loop.

```python
import asyncio
import requests # Synchronous blocking library

def blocking_io_network_call():
    response = requests.get('https://example.com')
    return response.status_code

async def main():
    # Push the blocking execution into the built-in thread pool
    loop = asyncio.get_running_loop()
    status = await loop.run_in_executor(None, blocking_io_network_call)
    print(status)
```

## Using `anyio` or Custom Architectures
For robust library design without coupling strictly to `asyncio` built-ins, standardizing on frameworks like `anyio` provides compatibility over different backends like `trio` enforcing strict task-groups and timeouts.
