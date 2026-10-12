"""Starter tests for BudgetFileHandler."""

import pytest


def test_read_transactions_csv(file_handler, tmp_path):
    """Read transactions from a simple CSV file."""
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-01,Payroll,Income,5000.00,income\n"
        "2026-06-02,Grocery,Groceries,120.00,expense\n",
        encoding="utf-8",
    )

    transactions = file_handler.read_transactions_csv("transactions.csv")

    assert len(transactions) == 2
    assert transactions[1]["amount"] == 120.0


def test_processed_files_are_tracked(file_handler, tmp_path):
    """Track files read by the handler."""
    csv_file = tmp_path / "transactions.csv"
    csv_file.write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-02,Grocery,Groceries,120.00,expense\n",
        encoding="utf-8",
    )

    file_handler.read_transactions_csv("transactions.csv")

    assert file_handler.get_processed_files() == ["transactions.csv"]


def test_file_operations_reject_paths_outside_base(file_handler, tmp_path):
    """Reject traversal and absolute paths for every file operation."""
    outside_file = tmp_path.parent / "outside.json"
    original_content = '[{"merchant": "private"}]'
    outside_file.write_text(original_content, encoding="utf-8")
    unsafe_filenames = (str(outside_file), f"..{outside_file.anchor[-1]}{outside_file.name}")

    for filename in unsafe_filenames:
        with pytest.raises(ValueError):
            file_handler.read_transactions_csv(filename)
        with pytest.raises(ValueError):
            file_handler.read_transactions_json(filename)
        with pytest.raises(ValueError):
            file_handler.write_report_json(filename, {"status": "overwritten"})

    assert outside_file.read_text(encoding="utf-8") == original_content
    assert file_handler.get_processed_files() == []