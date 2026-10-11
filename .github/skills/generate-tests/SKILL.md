---
name: generate-tests
description: Generate focused pytest coverage for Budget Buddy
disable-model-invocation: true
---
Generate focused pytest tests for the selected Budget Buddy module.

Requirements:
- Cover happy paths, edge cases, and error paths.
- Use existing fixtures from `tests/conftest.py` where they fit.
- Add tests before changing implementation when exposing a bug.
- Keep tests readable and grouped by behavior.
- Run `pytest` after changes.
- If coverage improves enough, recommend whether to raise the threshold in `pytest.ini`.