import runpy
from pathlib import Path

import pytest

import main as app


def test_build_report_calculates_totals(sample_transactions) -> None:
    report = app.build_report(1000.0, sample_transactions)
    assert report == {
        "monthly_budget": 1000.0, "income": 5000.0, "expenses": 160.0,
        "remaining_budget": 840.0, "net_cash_flow": 4840.0,
        "savings_rate": pytest.approx(96.8),
        "largest_expense": sample_transactions[1],
        "category_totals": {"Groceries": 120.0, "Transport": 40.0},
        "top_merchants": [
            {"merchant": "Grocery", "amount": 120.0},
            {"merchant": "Transit", "amount": 40.0},
        ],
    }


def test_build_report_without_transactions() -> None:
    assert app.build_report(1000.0, []) == {
        "monthly_budget": 1000.0, "income": 0, "expenses": 0,
        "remaining_budget": 1000.0, "net_cash_flow": 0,
        "savings_rate": 0.0, "largest_expense": None, "category_totals": {},
        "top_merchants": [],
    }


def test_show_top_merchants_formats_table(monkeypatch) -> None:
    messages = []
    monkeypatch.setattr(app.logger, "info", messages.append)
    app.show_top_merchants([
        {"merchant": "Grocery", "amount": 120.5},
        {"merchant": "Transit", "amount": 40.0},
    ])
    assert messages == [
        "Top merchants by spend", "Merchant             | Amount",
        "----------------------|----------", "Grocery              |  $120.50",
        "Transit              |   $40.00",
    ]


def test_show_top_merchants_handles_empty_input(monkeypatch) -> None:
    messages = []
    monkeypatch.setattr(app.logger, "info", messages.append)
    app.show_top_merchants([])
    assert messages == ["Top merchants by spend", "No expense transactions."]


@pytest.mark.parametrize("value,expected", [
    (1234.5, "$1,234.50"), (0, "$0.00"), (-12.5, "$-12.50"), ("2.5", "$2.50"),
])
def test_format_currency(value: object, expected: str) -> None:
    assert app.format_currency(value) == expected


def test_format_currency_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        app.format_currency("invalid")
    with pytest.raises(TypeError):
        app.format_currency(None)


def test_show_transactions_limits_output_to_first_page(monkeypatch, sample_transactions) -> None:
    messages = []
    monkeypatch.setattr(app.logger, "info", messages.append)
    transactions = [{**sample_transactions[1], "merchant": f"Shop {index}"}
                    for index in range(7)]
    app.show_transactions(transactions)
    assert messages[0] == "Recent transactions"
    assert len(messages) == 9
    assert "Shop 0" in messages[3]
    assert "$120.00" in messages[3]
    assert "Shop 5" in messages[-1]
    assert not any("Shop 6" in message for message in messages)


@pytest.mark.parametrize("as_script", [False, True])
def test_entry_point_reads_temporary_data(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, as_script: bool
) -> None:
    data = tmp_path / "data"
    data.mkdir()
    (data / "sample_transactions.csv").write_text(
        "date,merchant,category,amount,type\n"
        "2026-06-01,Payroll,Income,1000,income\n"
        "2026-06-02,Shop,Food,100,expense\n",
        encoding="utf-8",
    )
    messages = []
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(app.logger, "info", messages.append)
    if as_script:
        runpy.run_module("main", run_name="__main__")
    else:
        app.main()
    assert "Budget Buddy - GitHub Copilot Demo App" in messages
    assert "Monthly budget: $3,200.00" in messages
    assert "Income: $1,000.00" in messages
    assert "Expenses: $100.00" in messages
    assert "Remaining budget: $3,100.00" in messages
    assert "Net cash flow: $900.00" in messages
    assert "Savings rate: 90.0%" in messages
    assert "Category totals: {'Food': 100.0}" in messages
    assert "Top merchants by spend" in messages
    assert "Shop                 |  $100.00" in messages