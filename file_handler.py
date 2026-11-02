"""File loading helpers with confined paths and atomic report writes.

The base directory must not be writable by untrusted users: path validation
does not prevent concurrent symlink or junction replacement.
"""

import csv
from datetime import date
import json
import math
import ntpath
import os
from pathlib import Path
import tempfile
from typing import Dict, List


Transaction = Dict[str, object]
CSV_FIELDS = ("date", "merchant", "category", "amount", "type")


class BudgetFileHandler:
    """Read and write budget tracker data files."""

    def __init__(self, base_path: str = ".") -> None:
        """Initialize the handler with a base path."""
        self.base_path = base_path
        self.files_processed: List[str] = []

    def _resolve_safe_path(self, filename: str) -> Path:
        """Resolve a relative filename inside base_path, following links."""
        if not filename or ntpath.isabs(filename) or ntpath.splitdrive(filename)[0]:
            raise ValueError("Filename must be a nonempty relative path")

        base = Path(self.base_path).resolve()
        # Treat both Windows and POSIX separators as path separators.
        target = (base / filename.replace("\\", "/")).resolve()
        try:
            target.relative_to(base)
        except ValueError as exc:
            raise ValueError("Filename must remain inside base_path") from exc

        if target == base:
            raise ValueError("Filename must identify a file")
        return target

    def read_transactions_csv(self, filename: str) -> List[Transaction]:
        """Read transactions from a CSV file."""
        filepath = self._resolve_safe_path(filename)
        transactions: List[Transaction] = []

        with open(filepath, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file, strict=True)
            try:
                if reader.fieldnames is None or sorted(reader.fieldnames) != sorted(CSV_FIELDS):
                    raise ValueError("CSV header must contain date, merchant, category, amount, type")
                for row in reader:
                    transactions.append(self._validate_csv_row(row, reader.line_num))
            except csv.Error as exc:
                raise ValueError(f"CSV row {reader.line_num}: {exc}") from exc

        self.files_processed.append(filename)
        return transactions

    def _validate_csv_row(self, row: Transaction, line_number: int) -> Transaction:
        try:
            if set(row) != set(CSV_FIELDS):
                raise ValueError("incorrect number of columns")
            for field in CSV_FIELDS:
                if row[field] is None or not str(row[field]).strip():
                    raise ValueError(f"missing {field}")
            date.fromisoformat(str(row["date"]))
            amount = float(row["amount"])
            if not math.isfinite(amount) or amount < 0:
                raise ValueError("amount must be finite and nonnegative")
            if row["type"] not in ("income", "expense"):
                raise ValueError("type must be income or expense")
        except (KeyError, TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"CSV row {line_number}: {exc}") from exc
        return {**row, "amount": amount}

    def write_transactions_csv(self, filename: str, transactions: List[Transaction]) -> None:
        """Atomically export transactions using the reader's CSV columns."""
        filepath = self._resolve_safe_path(filename)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", newline="", dir=filepath.parent,
                prefix=".budget-transactions-", suffix=".tmp", delete=False,
            ) as file:
                temporary_path = Path(file.name)
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
                writer.writeheader()
                for line_number, transaction in enumerate(transactions, start=2):
                    writer.writerow(self._validate_csv_row(transaction, line_number))
                file.flush()
                os.fsync(file.fileno())
            os.replace(temporary_path, filepath)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
        self.files_processed.append(filename)

    def read_transactions_json(self, filename: str) -> List[Transaction]:
        """Read transactions from a JSON file."""
        filepath = self._resolve_safe_path(filename)
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
        self.files_processed.append(filename)
        return data

    def write_report_json(self, filename: str, report: Dict[str, object]) -> None:
        """Atomically replace a summary report inside base_path."""
        filepath = self._resolve_safe_path(filename)
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=filepath.parent,
                prefix=".budget-report-",
                suffix=".tmp",
                delete=False,
            ) as file:
                temporary_path = Path(file.name)
                json.dump(report, file, indent=2)
                file.flush()
                os.fsync(file.fileno())

            # Close the temporary file before replacement for Windows support.
            os.replace(temporary_path, filepath)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

        self.files_processed.append(filename)

    def get_processed_files(self) -> List[str]:
        """Return processed files."""
        return self.files_processed.copy()


# Backward-compatible alias used by older demo prompts.
FileHandler = BudgetFileHandler