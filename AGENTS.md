# AGENTS.md — Budget Buddy

Operating manual for AI agents working in this repository. Read this before making
changes.

## What this project is

Budget Buddy is a small Python budget tracker used for GitHub Copilot (GH-300)
demonstrations. It is intentionally a **working but immature** app. The main
branch provides the starter baseline, while feature branches may capture
completed workshop stages with higher coverage and selected issues resolved.

Do not remove the intentional issues unless the user explicitly asks to move
toward the completed/reference state. If you fix one, update
[INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) and [DEMO_SCRIPT.md](DEMO_SCRIPT.md).

## Environment and commands

```powershell
.\setup_demo.ps1                 # create venv and install deps
.\.venv\Scripts\Activate.ps1     # activate the environment
python main.py                   # run the app
pytest                           # run tests with coverage gate
pytest --cov=. --cov-report=term-missing
```

The coverage gate lives in [pytest.ini](pytest.ini). The starter baseline begins
at 30%; completed workshop branches can raise it as tests are added.

## Conventions

- Python only. Use pytest for tests.
- Use `logger` from [logger.py](logger.py) for app output, not `print`.
- Add type hints on public functions.
- Prefer small, readable functions.
- Update [CHANGELOG.md](CHANGELOG.md) for meaningful changes.

## Agent workflow expectations

1. Add or update tests first when practical.
2. Fix the narrowest relevant code path.
3. Run `pytest`.
4. Update docs and changelog when behavior changes.
5. Summarize the result and remaining risks.

## Related guidance

- Repo-wide rules: [.github/copilot-instructions.md](.github/copilot-instructions.md)
- Reusable task playbooks: [.github/skills](.github/skills)
