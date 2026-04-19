---
name: python-performance-optimization
description: Master profiling and optimization in Python (cProfile, memory_profiler, CPU optimization, and efficient data structures).
category: Python
license: Private
---

# Python Performance Optimization

## When to use this skill

Use this skill when you need to:
- Identify and resolve CPU or memory bottlenecks in Python codebases.
- Enhance the execution speed of data processing pipelines or worker scripts.
- Select the most appropriate, performant data structures for critical loops.
- Use built-in or external profilers to pinpoint exact lines causing slowdowns.

## Essential Tools for Profiling

### CPU Profiling

Always rely on actual data rather than guesses. `cProfile` provides a C-extension based profiler:

```bash
python -m cProfile -s cumtime my_script.py
```

For line-by-line inspection, install `line_profiler` and mark targeted functions with `@profile`:

```bash
kernprof -l -v my_script.py
```

### Memory Profiling

If memory exhaustion or leaks occur, utilize `memory_profiler`:

```python
from memory_profiler import profile

@profile
def my_memory_intensive_function():
    # Large calculations
    pass
```

## Anti-Patterns and Best Practices

### 1. The Global Interpreter Lock (GIL) is Not Always Your Enemy
- **I/O Bound**: Use `asyncio` or `threading` (e.g. web scraping, file I/O). The GIL drops on I/O.
- **CPU Bound**: Use `multiprocessing` to run tasks on separate cores, bypassing the GIL completely.

### 2. Data Structures
- Avoid adding/removing elements from the middle of a `list`. Use `collections.deque` for O(1) operations.
- Avoid iterating through a `list` to check for element existence (`if x in my_list`). Use `set` for O(1) lookups.

### 3. Vectorization over Loops
Native loops in Python are interpreted and comparatively slow. Instead of `for` loops to modify lists of numbers, use `numpy` vectorization.
```python
# Slow
[x * 2 for x in data]

# Fast (with numpy)
data_array * 2
```

## String Concatenation

Avoid the `+` operator in loops, which creates a new string on each iteration.
```python
# Slower
result = ""
for char in data:
    result += char

# Optimal
result = "".join(data)
```
