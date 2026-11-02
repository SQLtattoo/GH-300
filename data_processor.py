"""
Transaction processing helpers for the Budget Buddy demo app.

This module intentionally retains inefficient logic and permissive validation
so GitHub Copilot can improve it during the workshop.
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
        """Return normalized expense totals with a single pass over transactions."""
        self.processed_count += 1
        totals: Dict[str, float] = defaultdict(float)
        for expense in transactions:
            if expense.get("type") != "expense":
                continue
            category = self.normalize_category(str(expense.get("category", "")))
            totals[category] += float(expense.get("amount", 0))

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

    def sort_transactions(
        self, transactions: List[Transaction], field: str, descending: bool = False
    ) -> List[Transaction]:
        """Return a sorted copy, using numeric comparison for amounts."""
        if field not in ("date", "merchant", "category", "amount"):
            raise ValueError(f"Unsupported sort field: {field}")
        self.processed_count += 1
        if field == "amount":
            return sorted(transactions, key=lambda item: float(item[field]), reverse=descending)
        return sorted(transactions, key=lambda item: str(item[field]), reverse=descending)

    def spending_alerts(
        self, transactions: List[Transaction], category_limits: Dict[str, float]
    ) -> Dict[str, float]:
        """Return normalized categories and spending totals above their limits."""
        self.processed_count += 1
        totals: Dict[str, float] = defaultdict(float)
        for item in self.expenses_only(transactions):
            category = self.normalize_category(str(item.get("category", "")))
            totals[category] += float(item["amount"])
        limits = {self.normalize_category(category): limit
                  for category, limit in category_limits.items()}
        return {category: total for category, total in totals.items()
                if category in limits and total > limits[category]}

    def summarize_by_merchant(self, transactions: List[Transaction]) -> Dict[str, float]:
        """Return expense totals by merchant, excluding income."""
        self.processed_count += 1
        totals: Dict[str, float] = defaultdict(float)
        for item in self.expenses_only(transactions):
            totals[str(item["merchant"])] += float(item["amount"])
        return dict(totals)

    def top_merchants(
        self, transactions: List[Transaction], limit: int = 5
    ) -> List[Transaction]:
        """Return the highest-spend merchants, ordered by spend then name."""
        if limit < 0:
            raise ValueError("limit must be nonnegative")
        merchant_totals = self.summarize_by_merchant(transactions)
        ranked = sorted(
            merchant_totals.items(),
            key=lambda item: (-item[1], item[0].casefold(), item[0]),
        )
        return [
            {"merchant": merchant, "amount": amount}
            for merchant, amount in ranked[:limit]
        ]

    def get_processed_count(self) -> int:
        """Return the number of processing operations performed."""
        return self.processed_count


# Backward-compatible alias used by older demo prompts.
DataProcessor = TransactionProcessor