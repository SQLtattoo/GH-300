# Intentional Issues

Budget Buddy starts from a realistic but incomplete codebase. These issues are deliberate teaching material for GitHub Copilot demos.

## Bugs To Fix

| Module | Area | File | Issue | Demo Value |
| --- | --- | --- | --- | --- |
| 3 | Validation | [data_processor.py](data_processor.py) | Negative amounts and unknown transaction types are accepted | Input validation |
| 4 | CSV handling | [file_handler.py](file_handler.py) | Malformed CSV rows fail unclearly | Error handling |

## Performance Issues

| Module | File | Issue | Suggested Improvement |
| --- | --- | --- | --- |
| 3 | [data_processor.py](data_processor.py) | Duplicate detection is O(n^2) | Use a tuple key and dictionary/set |

## TODOs For Feature Generation

- `forecast_month_end_spend()` in [calculator.py](calculator.py)
- `is_over_budget()` in [calculator.py](calculator.py)
- `sort_transactions()` in [data_processor.py](data_processor.py)
- `spending_alerts()` in [data_processor.py](data_processor.py)
- `summarize_by_merchant()` in [data_processor.py](data_processor.py)
- `write_transactions_csv()` in [file_handler.py](file_handler.py)

## Resolved Issues

- Budget calculations return `0.0` for empty expense averages, zero-expense
  category percentages, and zero-income savings rates.
- File reads and writes in [file_handler.py](file_handler.py) now reject absolute
  paths and paths that resolve outside the configured base directory.
- Category grouping in [data_processor.py](data_processor.py) now aggregates
  expenses in a single pass.
- [Dockerfile](Dockerfile) now builds a runnable Budget Buddy image.
- [.github/workflows/ci.yml](.github/workflows/ci.yml) now installs test
  dependencies and runs pytest on pushes and pull requests.

## Coverage Journey

The starter suite intentionally covers only the happy path. Ask Copilot to add tests for:

- empty inputs
- zero-income months
- zero-expense months
- malformed CSV rows
- duplicate transactions
- category grouping behavior
- report-building behavior in [main.py](main.py)
- table behavior in [data_table.py](data_table.py)
- logging behavior in [logger.py](logger.py)