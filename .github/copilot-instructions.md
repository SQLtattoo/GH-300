# GitHub Copilot Instructions - Budget Buddy Demo Lab

Budget Buddy is a GH-300 training repository. Treat the codebase as a working
demo app, not as finished production software. The main branch may be used as
the starter baseline; feature branches can capture completed workshop stages.

## Important Context
- The app should run from `python main.py`.
- The current suite and coverage gate are defined in [pytest.ini](../pytest.ini).
- The trainer will use Copilot to generate tests, fix bugs, review security, refactor performance issues, and update docs.
- Do not remove intentional issues unless the user asks to move toward the completed/reference state.

## Required Patterns
- Python only.
- Use pytest for tests.
- Use `logger` from [logger.py](../logger.py) for app output.
- Use type hints on public functions.
- Prefer small, readable functions.

## Demo Issues To Preserve In Starter State
- Low coverage baseline.
- TODOs in calculator, transaction processor, and file handler modules.
- Edge-case bugs in budget calculations.
- Path traversal gap in JSON file reading.
- O(n^2) transaction processing logic.

When a user explicitly asks to complete a workshop stage, update the issue
ledger and demo documentation to reflect the new state.

## Change Workflow

- Before editing, identify which repository instructions affect the task.
- Add or update tests first when practical.
- Fix the narrowest relevant code path.
- Run `pytest` after code changes.
- Update `README.md` when setup, commands, or user-facing behavior changes.
- Update `CHANGELOG.md` for meaningful user-facing changes.
- Before committing, summarize changed files, tests run, and remaining risks.
