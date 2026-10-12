"""Starter tests for BudgetCalculator."""


def test_total_income(calculator, sample_transactions):
    """Calculate income for a happy-path transaction set."""
    assert calculator.total_income(sample_transactions) == 5000.0


def test_total_expenses(calculator, sample_transactions):
    """Calculate expenses for a happy-path transaction set."""
    assert calculator.total_expenses(sample_transactions) == 160.0


def test_remaining_budget(calculator, sample_transactions):
    """Calculate remaining budget for the sample month."""
    assert calculator.remaining_budget(1000.0, sample_transactions) == 840.0


def test_empty_transactions_have_zero_totals_and_preserve_budget(calculator):
    """Treat an empty month as having no income or expenses."""
    assert calculator.total_income([]) == 0.0
    assert calculator.total_expenses([]) == 0.0
    assert calculator.net_cash_flow([]) == 0.0
    assert calculator.remaining_budget(1000.0, []) == 1000.0


def test_average_expense_is_zero_when_there_are_no_expenses(calculator):
    """Return zero when transactions contain no expenses to average."""
    income_only = [{"type": "income", "amount": 5000.0}]

    assert calculator.average_expense(income_only) == 0.0


def test_category_percentage_is_zero_when_total_expenses_are_zero(calculator):
    """Avoid an undefined percentage when no expenses were recorded."""
    assert calculator.category_percentage(0.0, 0.0) == 0.0


def test_savings_rate_is_zero_when_income_is_zero(calculator):
    """Avoid an undefined savings rate for a zero-income month."""
    assert calculator.savings_rate(0.0, 100.0) == 0.0


def test_history_records_nested_operations_and_returns_a_copy(calculator, sample_transactions):
    """Keep operations ordered and protect internal history from mutation."""
    calculator.net_cash_flow(sample_transactions)

    history = calculator.get_history()
    assert history == [
        "total_income = 5000.0",
        "total_expenses = 160.0",
        "net_cash_flow = 4840.0",
    ]

    history.append("tampered")
    assert "tampered" not in calculator.get_history()