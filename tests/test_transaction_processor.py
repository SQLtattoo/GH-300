"""Starter tests for TransactionProcessor."""


def test_filter_by_month(processor, sample_transactions):
    """Filter transactions by a YYYY-MM prefix."""
    assert processor.filter_by_month(sample_transactions, "2026-06") == sample_transactions


def test_largest_expense(processor, sample_transactions):
    """Find the largest expense on the happy path."""
    largest = processor.largest_expense(sample_transactions)
    assert largest["merchant"] == "Grocery"


def test_group_expenses_by_category_aggregates_in_one_pass(processor):
    """Aggregate normalized expense categories while ignoring income."""
    transactions = [
        {"category": " groceries ", "amount": 10.0, "type": "expense"},
        {"category": "GROCERIES", "amount": 15.5, "type": "expense"},
        {"category": "Transport", "amount": 8.0, "type": "expense"},
        {"category": "Groceries", "amount": 100.0, "type": "income"},
    ]

    assert processor.group_expenses_by_category(transactions) == {
        "Groceries": 25.5,
        "Transport": 8.0,
    }


def test_validate_transaction_accepts_required_fields(processor, sample_transactions):
    """Validate a complete happy-path transaction."""
    assert processor.validate_transaction(sample_transactions[0]) is True