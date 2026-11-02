# Intentional Issues

Budget Buddy starts from a realistic but incomplete codebase. These issues are deliberate teaching material for GitHub Copilot demos.

## Bugs To Fix

| Module | Area | File | Issue | Demo Value |
| --- | --- | --- | --- | --- |
| 4 | Edge cases | [calculator.py](calculator.py) | Empty expense lists raise `ZeroDivisionError` | Bug fixing + tests |
| 4 | Edge cases | [calculator.py](calculator.py) | Category percentage divides by zero | Defensive programming |
| 4 | Edge cases | [calculator.py](calculator.py) | Savings rate divides by zero when income is zero | Test-driven bug fix |
| 3 | Validation | [data_processor.py](data_processor.py) | Negative amounts and unknown transaction types are accepted | Input validation |
| 2 | Security | [file_handler.py](file_handler.py) | JSON reads do not validate paths | Security review |
| 4 | CSV handling | [file_handler.py](file_handler.py) | Malformed CSV rows fail unclearly | Error handling |

## Performance Issues

| Module | File | Issue | Suggested Improvement |
| --- | --- | --- | --- |
| 3 | [data_processor.py](data_processor.py) | Category grouping mutates a list while using nested loops | Replace with one-pass aggregation |
| 3 | [data_processor.py](data_processor.py) | Duplicate detection is O(n^2) | Use a tuple key and dictionary/set |

## Completed DevOps Work (Module 3)

| File | Completed behavior | Verification |
| --- | --- | --- |
| [Dockerfile](Dockerfile) | Python 3.13 slim image, dependencies, app/data copy, and `python main.py` | Build and run with Docker Desktop's Linux engine running |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Python 3.13 setup, dependency install, and pytest with the existing coverage gate | Push or open a PR targeting main |

## TODOs For Feature Generation

- `forecast_month_end_spend()` in [calculator.py](calculator.py)
- `is_over_budget()` in [calculator.py](calculator.py)
- `sort_transactions()` in [data_processor.py](data_processor.py)
- `spending_alerts()` in [data_processor.py](data_processor.py)
- `summarize_by_merchant()` in [data_processor.py](data_processor.py)
- `write_transactions_csv()` in [file_handler.py](file_handler.py)
- `_resolve_safe_path()` in [file_handler.py](file_handler.py)

## Coverage Journey

The starter suite intentionally covers only the happy path. Ask Copilot to add tests for:

- empty inputs
- zero-income months
- zero-expense months
- malformed CSV rows
- path traversal attempts
- duplicate transactions
- category grouping behavior
- report-building behavior in [main.py](main.py)
- table behavior in [data_table.py](data_table.py)
- logging behavior in [logger.py](logger.py)