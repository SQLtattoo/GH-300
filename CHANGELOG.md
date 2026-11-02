# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Added a top-five merchants-by-spend section to the monthly report, excluding
	income and sorting ties deterministically by merchant name.
- Added table workflow and application report/entry-point tests, bringing the
	configured total coverage above 90% without changing application behavior.
- Implemented expense forecasting, over-budget checks, transaction sorting,
  normalized category spending alerts, and expense totals by merchant.
- Added validated, path-confined atomic CSV export and clear CSV row errors.
- Added regression tests for feature boundaries, CSV validation, and export safety.
- Added security regression tests for path containment and atomic report writes.
- Revamped the repository into **Budget Buddy**, a working Personal Budget & Expense Tracker demo app for GH-300 delivery.
- Added sample transaction data in [data/sample_transactions.csv](data/sample_transactions.csv).
- Added a sparse starter pytest suite designed to begin around 30% coverage.
- Added [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for trainer delivery flow.
- Added [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) documenting deliberate bugs, TODOs, security gaps, and performance issues.
- Added reusable Copilot Skills under [.github/skills](.github/skills).

### Changed
- Documented calculator public methods, including existing zero-division behavior;
	retained their existing parameter and return type hints without behavior changes.
- Refactored category grouping into a single-pass aggregation with one category
	normalization per expense, preserving input data and expense-only totals.
- Completed Docker and GitHub Actions setup, including dependency installation
	and the existing pytest coverage gate. CI uses pip caching and read-only
	repository permissions; the image copies app/data without local environments
	or Git metadata. Updated demo completion notes.
- Confined CSV/JSON reads and report writes to `base_path`, rejecting absolute,
	drive-qualified, and escaping paths, including existing symlink/junction targets.
- Write JSON reports through same-directory temporary files with atomic
	replacement and cleanup, preserving existing reports when writes fail.
- Updated security demo documentation; unrelated intentional issues remain.
- Simplified console logging to show report messages without timestamp, logger name, or level prefixes.
- Replaced arithmetic-only calculator examples with budget calculation helpers.
- Replaced generic data processing examples with transaction processing helpers.
- Replaced generic file examples with CSV/JSON budget data loading helpers.
- Updated pytest configuration to use a demo-start `30%` coverage threshold.
- Refreshed README, quick reference, setup script, reset script, and Copilot instructions for the app-centered demo flow.

### Intentional Demo Gaps
- Coverage is intentionally low at the start of the demo.
- Original code TODOs are complete; unrelated calculator bugs and permissive
	transaction-processor validation remain for Copilot-assisted exercises.
- CSV handling and path traversal are now fixed
	subject to a trusted filesystem (concurrent link replacement remains a risk).
- Transaction processing intentionally includes O(n^2) logic for refactoring demos.