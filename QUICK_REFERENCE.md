# Budget Buddy Demo Quick Reference

## Commands

```powershell
.\setup_demo.ps1
.\.venv\Scripts\Activate.ps1
python main.py
pytest
pytest --cov=. --cov-report=term-missing
```

## Baseline

- App should run successfully.
- Starter tests should pass.
- Coverage should be around 30%.
- The demo objective is 90%+ coverage after Copilot assistance.

## High-Value Demo Targets (by GH-300 module)

| Module | Capability | File | Prompt |
| --- | --- | --- | --- |
| 1 | Run the app | [main.py](main.py) | `python main.py` to prove it works. |
| 2 | Explain codebase | Workspace | `Explain this app and identify the core flow.` |
| 2 | Inline Chat / security prompt | [file_handler.py](file_handler.py) | `Review file handling for path traversal risks.` |
| 3 | Refactor performance | [data_processor.py](data_processor.py) | `Refactor inefficient transaction processing while preserving behavior.` |
| 3 | DevOps snippets | [Dockerfile](Dockerfile), [.github/workflows/ci.yml](.github/workflows/ci.yml) | `Finish the Dockerfile and CI workflow to run pytest.` |
| 4 | Generate tests | [tests](tests) | `Use the generate-tests prompt and raise coverage toward 90%.` |
| 4 | Fix bugs | [calculator.py](calculator.py) | `Find edge cases in BudgetCalculator and fix them with tests.` |
| 5 | Agent mode | Multiple files | `Add CSV export with tests, docs, and changelog updates.` |
| 5 | AGENTS.md / Skills | [AGENTS.md](AGENTS.md), [.github/skills](.github/skills) | Show the agent operating manual and a `SKILL.md` playbook. |
| 5 | PR summary | Git diff | `Summarize this diff as a pull request description.` |

## Remaining Intentional Issues

- `TransactionProcessor.find_duplicate_transactions()` uses O(n^2) duplicate detection.
- `TransactionProcessor.validate_transaction()` accepts negative amounts and unknown types.
- CSV parsing lacks clear errors for malformed rows.
- TODOs are present for budget alerts, CSV export, sorting, merchant summaries, and spending alerts.