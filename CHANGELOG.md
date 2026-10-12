# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- Revamped the repository into **Budget Buddy**, a working Personal Budget & Expense Tracker demo app for GH-300 delivery.
- Added sample transaction data in [data/sample_transactions.csv](data/sample_transactions.csv).
- Added a sparse starter pytest suite designed to begin around 30% coverage.
- Added [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for trainer delivery flow.
- Added [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md) documenting deliberate bugs, TODOs, security gaps, and performance issues.
- Added reusable Copilot Skills under [.github/skills](.github/skills).

### Changed
- Simplified console logging to show report messages without timestamp, logger name, or level prefixes.
- Replaced arithmetic-only calculator examples with budget calculation helpers.
- Replaced generic data processing examples with transaction processing helpers.
- Replaced generic file examples with CSV/JSON budget data loading helpers.
- Updated pytest configuration to use a demo-start `30%` coverage threshold.
- Refreshed README, quick reference, setup script, reset script, and Copilot instructions for the app-centered demo flow.

### Intentional Demo Gaps
- Coverage is intentionally low at the start of the demo.
- Several TODOs and bugs are intentionally present for Copilot-assisted implementation.
- File handling intentionally includes a path traversal risk for security review demos.
- Transaction processing intentionally includes O(n^2) logic for refactoring demos.