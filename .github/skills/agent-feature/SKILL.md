---
name: agent-feature
description: Implement a multi-file Budget Buddy feature
disable-model-invocation: true
---
Implement the requested Budget Buddy feature across code, tests, and docs.

Expected workflow:
- inspect the relevant modules
- add or update tests
- implement the feature
- update `README.md` if commands or behavior change
- update `CHANGELOG.md`
- run `pytest`
- summarize files changed, tests run, and remaining risks

Good demo feature ideas:
- CSV export
- month-end spending forecast
- category spending alerts
- merchant summaries
- safe path resolution for all file operations