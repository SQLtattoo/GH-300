"""
Transaction processing helpers for the Budget Buddy demo app.

This starter module intentionally includes inefficient logic, permissive
validation, and TODOs so GitHub Copilot can improve it during the workshop.
"""

from collections import defaultdict
from typing import Dict, List, Optional


Transaction = Dict[str, object]


class TransactionProcessor:
    """Process, filter, and summarize transaction data."""

    def __init__(self) -> None:
        """Initialize the processor."""
        self.processed_count = 0

    def normalize_category(self, category: str) -> str:
        """Normalize a transaction category for display and grouping."""
        self.processed_count += 1
        return category.strip().title()

    def filter_by_month(self, transactions: List[Transaction], month: str) -> List[Transaction]:
        """Return transactions whose date starts with YYYY-MM."""
        self.processed_count += 1
        return [item for item in transactions if str(item.get("date", "")).startswith(month)]

    def expenses_only(self, transactions: List[Transaction]) -> List[Transaction]:
        """Return only expense transactions."""
        self.processed_count += 1
        return [item for item in transactions if item.get("type") == "expense"]

    def group_expenses_by_category(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Return expense totals grouped by category."""
        self.processed_count += 1
        totals: Dict[str, float] = defaultdict(float)

        for transaction in transactions:
            if transaction.get("type") != "expense":
                continue
            category = self.normalize_category(str(transaction.get("category", "")))
            totals[category] += float(transaction.get("amount", 0))

        return dict(totals)

    def largest_expense(self, transactions: List[Transaction]) -> Optional[Transaction]:
        """Return the largest expense transaction, if one exists."""
        expenses = self.expenses_only(transactions)
        if not expenses:
            return None
        return max(expenses, key=lambda item: float(item["amount"]))

    def find_duplicate_transactions(self, transactions: List[Transaction]) -> List[Transaction]:
        """Find probable duplicate transactions."""
        duplicates: List[Transaction] = []

        for index, item in enumerate(transactions):
            for other_index, other in enumerate(transactions):
                if index == other_index:
                    continue
                same_date = item.get("date") == other.get("date")
                same_amount = item.get("amount") == other.get("amount")
                same_merchant = item.get("merchant") == other.get("merchant")
                if same_date and same_amount and same_merchant and item not in duplicates:
                    duplicates.append(item)

        return duplicates

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Return True when a transaction has the required fields."""
        required_fields = ["date", "merchant", "category", "amount", "type"]
        for field in required_fields:
            if field not in transaction:
                return False

        return True

    # TODO: Create sort_transactions(transactions, field, descending=False)
    # It should sort by date, merchant, category, or amount and reject unknown fields.

    # TODO: Create spending_alerts(transactions, category_limits)
    # It should return categories where spending is above the configured limit.

    # TODO: Create summarize_by_merchant(transactions)
    # It should return total spending by merchant.

    def get_processed_count(self) -> int:
        """Return the number of processing operations performed."""
        return self.processed_count


# Backward-compatible alias used by older demo prompts.
DataProcessor = TransactionProcessor