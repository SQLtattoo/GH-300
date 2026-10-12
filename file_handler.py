"""
File loading helpers for the Budget Buddy demo app.

File access is restricted to the configured base directory.
"""

import csv
import json
from pathlib import Path
from typing import Dict, List


Transaction = Dict[str, object]


class BudgetFileHandler:
    """Read and write budget tracker data files."""

    def __init__(self, base_path: str = ".") -> None:
        """Initialize the handler with a base path."""
        self.base_path = base_path
        self.files_processed: List[str] = []

    def _resolve_safe_path(self, filename: str) -> Path:
        """Resolve a filename and ensure it remains inside the base path."""
        requested_path = Path(filename)
        if requested_path.is_absolute():
            raise ValueError("Absolute file paths are not allowed")

        base_path = Path(self.base_path).resolve()
        filepath = (base_path / requested_path).resolve()
        try:
            filepath.relative_to(base_path)
        except ValueError as error:
            raise ValueError("File path must remain inside the base path") from error

        return filepath

    def read_transactions_csv(self, filename: str) -> List[Transaction]:
        """Read transactions from a CSV file."""
        filepath = self._resolve_safe_path(filename)
        transactions: List[Transaction] = []

        with open(filepath, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                transactions.append(
                    {
                        "date": row["date"],
                        "merchant": row["merchant"],
                        "category": row["category"],
                        "amount": float(row["amount"]),
                        "type": row["type"],
                    }
                )

        self.files_processed.append(filename)
        return transactions

    def read_transactions_json(self, filename: str) -> List[Transaction]:
        """Read transactions from a JSON file."""
        filepath = self._resolve_safe_path(filename)
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.files_processed.append(filename)
        return data

    def write_report_json(self, filename: str, report: Dict[str, object]) -> None:
        """Write a summary report as JSON."""
        filepath = self._resolve_safe_path(filename)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=2)
        self.files_processed.append(filename)

    def get_processed_files(self) -> List[str]:
        """Return processed files."""
        return self.files_processed.copy()

    # TODO: Create write_transactions_csv(filename, transactions)
    # It should preserve the same CSV headers used by read_transactions_csv.

    # TODO: Improve read_transactions_csv to reject malformed rows with clear errors.


# Backward-compatible alias used by older demo prompts.
FileHandler = BudgetFileHandler