---
name: refactor-performance
description: Refactor inefficient Budget Buddy code
disable-model-invocation: true
---
Refactor the selected Budget Buddy code for performance while preserving behavior.

Requirements:
- Identify the inefficient algorithm and its complexity.
- Add tests that lock the current expected behavior.
- Replace O(n^2) loops with dictionary, set, or one-pass aggregation where appropriate.
- Keep public APIs stable unless the user asks otherwise.
- Run `pytest` and summarize the complexity improvement.