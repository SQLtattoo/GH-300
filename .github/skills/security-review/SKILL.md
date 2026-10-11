---
name: security-review
description: Review Budget Buddy for security issues
disable-model-invocation: true
---
Review the selected Budget Buddy code for security risks.

Focus on:
- path traversal
- unsafe file reads/writes
- malformed input handling
- confusing validation errors

For any issue found:
- explain the risk briefly
- add a failing pytest test that demonstrates it
- fix the smallest relevant code path
- rerun `pytest`
- update `CHANGELOG.md` and `INTENTIONAL_ISSUES.md` if the starter issue changes