# Budget Buddy - GitHub Copilot Demo Lab

Budget Buddy is a small Python budget tracker designed for Microsoft GH-300 demonstrations. It is intentionally a **working but immature** app: the happy path runs, starter tests pass, coverage is low, and realistic TODOs, bugs, security issues, and performance problems are left for GitHub Copilot to improve.

The goal is to show Copilot as more than autocomplete: codebase explanation, inline edits, agent mode, test generation, debugging, security review, refactoring, documentation, and PR-style summaries.

## Current Demo State

- Runnable app: `python main.py`
- Starter tests: 8 tests
- Current coverage target: about 30%
- Workshop goal: use Copilot to reach 90%+ coverage
- Intentional issues: documented in [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md)
- Trainer flow: documented in [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

## Quick Start

```powershell
.\setup_demo.ps1
.\.venv\Scripts\Activate.ps1
python main.py
pytest
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## What The App Does

Budget Buddy reads sample transactions from [data/sample_transactions.csv](data/sample_transactions.csv), builds a simple monthly budget report, and logs:

- income
- expenses
- remaining budget
- net cash flow
- savings rate
- largest expense
- spending by category
- a paginated transaction table

## Main Files

| File | Purpose |
| --- | --- |
| [main.py](main.py) | Runnable demo app and report orchestration |
| [calculator.py](calculator.py) | Budget calculations with intentional edge-case bugs |
| [data_processor.py](data_processor.py) | Transaction filtering, grouping, duplicate detection, and TODOs |
| [file_handler.py](file_handler.py) | CSV/JSON file I/O with an intentional path traversal gap |
| [data_table.py](data_table.py) | Generic table helper used by the app |
| [logger.py](logger.py) | Centralized logging utility |
| [tests](tests) | Sparse starter tests for the coverage journey |

## Demo Flow (GH-300 modules)

The trainer flow in [DEMO_SCRIPT.md](DEMO_SCRIPT.md) is aligned to the five
course modules:

1. **Module 1 — Introduction:** run `setup_demo.ps1` and `python main.py` to frame the use case.
2. **Module 2 — Exploring Features:** Chat, Inline Chat, CLI, and focused context (security review of file handling).
3. **Module 3 — Developer Use Cases:** generate, transform, optimize, document, and a DevOps beat (Dockerfile + CI).
4. **Module 4 — Building Unit Tests:** the coverage journey from ~30% to 90%+.
5. **Module 5 — Advanced Capabilities:** Agent Mode, `AGENTS.md`, Skills, MCP, and PR review/summary.

## Useful Copilot Skills

Reusable task playbooks live in [.github/skills](.github/skills):

- `generate-tests`
- `security-review`
- `refactor-performance`
- `agent-feature`
- `devops-snippet`
- `pr-summary`
- `run-coverage`
- `add-budget-report-section`

## Agent Customization Assets

Module 5 showcases how Copilot follows project-level guidance:

- [AGENTS.md](AGENTS.md) — operating manual for agents in this repo.
- [.github/copilot-instructions.md](.github/copilot-instructions.md) — repo-wide rules.
- [.github/skills](.github/skills) — task playbooks (`SKILL.md`), e.g. adding a budget report section.

## Validation Commands

```powershell
python main.py
pytest
pytest --cov=. --cov-report=term-missing
```

During the demo, after Copilot generates enough tests and fixes, change the coverage threshold in [pytest.ini](pytest.ini) from `30` to `90` and rerun `pytest`.

## Trainer Notes

This repository is intentionally not production-ready. Do not remove the TODOs and bugs from the starter state unless you also update [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) and [DEMO_SCRIPT.md](DEMO_SCRIPT.md).