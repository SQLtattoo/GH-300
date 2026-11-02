"""Regression tests for confined paths and atomic report writes."""

import json
from pathlib import Path

import pytest

from file_handler import BudgetFileHandler


OPERATIONS = [
    "read_transactions_csv",
    "read_transactions_json",
    "write_report_json",
]


def _perform(handler: BudgetFileHandler, operation: str, filename: str) -> None:
    method = getattr(handler, operation)
    if operation == "write_report_json":
        method(filename, {"total": 25})
    else:
        method(filename)


@pytest.mark.parametrize("operation", OPERATIONS)
@pytest.mark.parametrize(
    "filename",
    [
        "../outside.json",
        r"..\outside.json",
        "../base-sibling/outside.json",
        r"C:\outside.json",
        "C:outside.json",
        r"\outside.json",
        r"\\server\share\outside.json",
        "",
        ".",
    ],
)
def test_rejects_unsafe_paths(
    tmp_path: Path, operation: str, filename: str
) -> None:
    base = tmp_path / "base"
    base.mkdir()
    handler = BudgetFileHandler(str(base))

    with pytest.raises(ValueError):
        _perform(handler, operation, filename)

    assert handler.get_processed_files() == []
    assert list(base.iterdir()) == []


@pytest.mark.parametrize("operation", OPERATIONS)
def test_rejects_absolute_paths(tmp_path: Path, operation: str) -> None:
    handler = BudgetFileHandler(str(tmp_path))

    with pytest.raises(ValueError):
        _perform(handler, operation, str(tmp_path / "outside.json"))

    assert handler.get_processed_files() == []


@pytest.mark.parametrize("operation", OPERATIONS)
def test_rejects_posix_absolute_paths(tmp_path: Path, operation: str) -> None:
    handler = BudgetFileHandler(str(tmp_path))

    with pytest.raises(ValueError):
        _perform(handler, operation, "/tmp/outside.json")

    assert handler.get_processed_files() == []


@pytest.mark.parametrize("operation", OPERATIONS)
def test_rejects_symlink_escape(tmp_path: Path, operation: str) -> None:
    base = tmp_path / "base"
    base.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    try:
        (base / "link").symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip("Symlink creation requires platform support and permissions")

    handler = BudgetFileHandler(str(base))
    with pytest.raises(ValueError):
        _perform(handler, operation, "link/report.json")

    assert handler.get_processed_files() == []
    assert list(outside.iterdir()) == []


def test_valid_nested_files(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    transactions = [{"merchant": "Grocery", "amount": 12.5}]
    (nested / "transactions.json").write_text(
        json.dumps(transactions), encoding="utf-8"
    )
    (nested / "transactions.csv").write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-02,Grocery,Groceries,12.5,expense\n",
        encoding="utf-8",
    )
    handler = BudgetFileHandler(str(tmp_path))

    assert handler.read_transactions_json("nested/transactions.json") == transactions
    assert handler.read_transactions_csv("nested/transactions.csv")[0]["amount"] == 12.5
    destination = nested / "report.json"
    destination.write_text('{"old": true}', encoding="utf-8")
    handler.write_report_json("nested/report.json", {"total": 12.5})

    assert json.loads(destination.read_text(encoding="utf-8")) == {"total": 12.5}
    assert handler.get_processed_files() == [
        "nested/transactions.json", "nested/transactions.csv", "nested/report.json"
    ]
    assert sorted(path.name for path in nested.iterdir()) == [
        "report.json", "transactions.csv", "transactions.json"
    ]


def test_failed_serialization_preserves_report(tmp_path: Path) -> None:
    destination = tmp_path / "report.json"
    original = '{"original": true}'
    destination.write_text(original, encoding="utf-8")
    handler = BudgetFileHandler(str(tmp_path))

    with pytest.raises(TypeError):
        handler.write_report_json("report.json", {"invalid": object()})

    assert destination.read_text(encoding="utf-8") == original
    assert list(tmp_path.iterdir()) == [destination]
    assert handler.get_processed_files() == []


def test_failed_replace_preserves_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    destination = tmp_path / "report.json"
    original = '{"original": true}'
    destination.write_text(original, encoding="utf-8")
    handler = BudgetFileHandler(str(tmp_path))

    def fail_replace(source: Path, target: Path) -> None:
        raise PermissionError("Replacement denied")

    monkeypatch.setattr("file_handler.os.replace", fail_replace)
    with pytest.raises(PermissionError):
        handler.write_report_json("report.json", {"total": 25})

    assert destination.read_text(encoding="utf-8") == original
    assert list(tmp_path.iterdir()) == [destination]
    assert handler.get_processed_files() == []
