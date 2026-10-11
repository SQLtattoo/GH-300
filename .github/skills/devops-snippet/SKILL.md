---
name: devops-snippet
description: Generate or complete DevOps assets for Budget Buddy
disable-model-invocation: true
---
Help complete the DevOps assets in this repository.

Targets:
- [Dockerfile](../../../Dockerfile): finish the image so `python main.py` runs in a container.
- [.github/workflows/ci.yml](../../workflows/ci.yml): finish the pipeline so it installs
  dependencies from `requirements-test.txt` and runs `pytest`.

Expected workflow:
- inspect the existing TODOs in each file
- complete the missing steps using current, pinned action versions
- keep the Python version consistent with the rest of the repo
- explain each change briefly
- if asked, validate the Dockerfile build and the workflow syntax
