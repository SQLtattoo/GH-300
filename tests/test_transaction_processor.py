"""Starter tests for TransactionProcessor."""

import pytest

from data_processor import TransactionProcessor


def test_filter_by_month(processor, sample_transactions):
    """Filter transactions by a YYYY-MM prefix."""
    assert processor.filter_by_month(sample_transactions, "2026-06") == sample_transactions


def test_largest_expense(processor, sample_transactions):
    """Find the largest expense on the happy path."""
    largest = processor.largest_expense(sample_transactions)
    assert largest["merchant"] == "Grocery"


def test_validate_transaction_accepts_required_fields(processor, sample_transactions):
    """Validate a complete happy-path transaction."""
    assert processor.validate_transaction(sample_transactions[0]) is True


def test_group_expenses_normalizes_categories_and_preserves_input(processor) -> None:
    transactions = [
        {"type": "expense", "category": " food ", "amount": "10.5"},
        {"type": "income", "category": "Food", "amount": 1000},
        {"type": "expense", "category": "FOOD", "amount": 2.5},
        {"type": "expense", "category": "Travel", "amount": 5},
        {"type": "expense"},
        {"category": "Food", "amount": 100},
    ]
    original = [item.copy() for item in transactions]
    assert processor.group_expenses_by_category(transactions) == {
        "Food": 13.0, "Travel": 5.0, "": 0.0,
    }
    assert transactions == original
    assert processor.group_expenses_by_category([]) == {}


def test_empty_expense_selection(processor) -> None:
    transactions = [{"type": "income", "amount": 100}]
    assert processor.expenses_only(transactions) == []
    assert processor.largest_expense(transactions) is None
    assert processor.largest_expense([]) is None


def test_duplicate_detection_uses_date_amount_and_merchant(processor) -> None:
    first = {"date": "2026-06-02", "amount": 10, "merchant": "Shop", "category": "Food"}
    matching = {**first, "category": "Other"}
    transactions = [first, first.copy(), matching,
                    {**first, "date": "2026-06-03"},
                    {**first, "amount": 11}, {**first, "merchant": "Cafe"}]
    original = [item.copy() for item in transactions]
    assert processor.find_duplicate_transactions(transactions) == [first, matching]
    assert transactions == original
    assert processor.find_duplicate_transactions([]) == []
    assert processor.find_duplicate_transactions([first]) == []


@pytest.mark.parametrize("field", ["date", "merchant", "category", "amount", "type"])
def test_validation_rejects_missing_fields(processor, sample_transactions, field: str) -> None:
    transaction = sample_transactions[0].copy()
    del transaction[field]
    assert processor.validate_transaction(transaction) is False


@pytest.mark.parametrize("field", ["date", "merchant", "category", "amount"])
@pytest.mark.parametrize("descending", [False, True])
def test_sort_transactions_preserves_input(
    processor, sample_transactions, field: str, descending: bool
) -> None:
    original = sample_transactions.copy()
    result = processor.sort_transactions(sample_transactions, field, descending)
    assert result == sorted(original, key=lambda item: item[field], reverse=descending)
    assert result is not sample_transactions
    assert sample_transactions == original


def test_sort_amounts_numerically_and_reject_invalid_input(processor) -> None:
    transactions = [{"amount": "100"}, {"amount": "20"}]
    assert processor.sort_transactions(transactions, "amount") == transactions[::-1]
    assert processor.sort_transactions([], "date") == []
    with pytest.raises(ValueError, match="Unsupported sort field"):
        processor.sort_transactions([], "type")
    with pytest.raises(ValueError):
        processor.sort_transactions([{"amount": "invalid"}], "amount")
    with pytest.raises(KeyError, match="amount"):
        processor.sort_transactions([{}], "amount")


def test_spending_alerts_normalize_categories_and_apply_strict_limits(processor) -> None:
    transactions = [
        {"type": "expense", "category": " food ", "amount": "10"},
        {"type": "expense", "category": "FOOD", "amount": 15},
        {"type": "expense", "category": "Travel", "amount": 20},
        {"type": "expense", "category": "Other", "amount": 100},
        {"type": "income", "category": "Food", "amount": 1000},
    ]
    assert processor.spending_alerts(transactions, {"food": 20, " Travel ": 20}) == {"Food": 25}
    assert processor.spending_alerts(transactions, {}) == {}
    assert processor.spending_alerts([], {"Food": 0}) == {}


def test_summarize_by_merchant_excludes_income(processor) -> None:
    transactions = [
        {"type": "expense", "merchant": "Shop", "amount": "10"},
        {"type": "expense", "merchant": "Shop", "amount": 15},
        {"type": "expense", "merchant": "Cafe", "amount": 5},
        {"type": "income", "merchant": "Shop", "amount": 1000},
    ]
    assert processor.summarize_by_merchant(transactions) == {"Shop": 25, "Cafe": 5}
    assert processor.summarize_by_merchant([]) == {}


def test_top_merchants_ranks_expenses_with_stable_ties(processor) -> None:
    transactions = [
        {"type": "expense", "merchant": "Zeta", "amount": 30},
        {"type": "expense", "merchant": "Beta", "amount": 50},
        {"type": "expense", "merchant": "Alpha", "amount": 50},
        {"type": "expense", "merchant": "Zeta", "amount": 25},
        {"type": "income", "merchant": "Payroll", "amount": 1000},
    ]
    assert processor.top_merchants(transactions, limit=2) == [
        {"merchant": "Zeta", "amount": 55.0},
        {"merchant": "Alpha", "amount": 50.0},
    ]
    assert processor.top_merchants(transactions) == [
        {"merchant": "Zeta", "amount": 55.0},
        {"merchant": "Alpha", "amount": 50.0},
        {"merchant": "Beta", "amount": 50.0},
    ]
    assert processor.top_merchants([], limit=5) == []
    assert processor.top_merchants(transactions, limit=0) == []
    with pytest.raises(ValueError, match="limit"):
        processor.top_merchants(transactions, limit=-1)


def test_processed_count_tracks_operations() -> None:
    processor = TransactionProcessor()
    assert processor.get_processed_count() == 0
    assert processor.normalize_category(" food ") == "Food"
    assert processor.get_processed_count() == 1