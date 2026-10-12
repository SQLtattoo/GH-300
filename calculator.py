"""
Financial calculation helpers for the Budget Buddy demo app.

This module is intentionally starter-quality for GitHub Copilot demos. Some
methods work on the happy path, while selected edge cases and TODOs are left for
learners to fix with Copilot.
"""

from typing import Dict, List


Transaction = Dict[str, object]


class BudgetCalculator:
    """Calculate budget metrics and retain a history of operations."""

    def __init__(self) -> None:
        """Initialize an empty calculation history."""
        self.history: List[str] = []

    def total_income(self, transactions: List[Transaction]) -> float:
        """Return the total amount of income transactions."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "income")
        self.history.append(f"total_income = {total}")
        return total

    def total_expenses(self, transactions: List[Transaction]) -> float:
        """Return the total amount of expense transactions."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "expense")
        self.history.append(f"total_expenses = {total}")
        return total

    def net_cash_flow(self, transactions: List[Transaction]) -> float:
        """Return income minus expenses."""
        result = self.total_income(transactions) - self.total_expenses(transactions)
        self.history.append(f"net_cash_flow = {result}")
        return result

    def remaining_budget(self, monthly_budget: float, transactions: List[Transaction]) -> float:
        """Return the monthly budget remaining after expenses."""
        result = monthly_budget - self.total_expenses(transactions)
        self.history.append(f"remaining_budget({monthly_budget}) = {result}")
        return result

    def average_expense(self, transactions: List[Transaction]) -> float:
        """Return the mean amount of expense transactions."""
        expenses = [float(item["amount"]) for item in transactions if item.get("type") == "expense"]
        result = sum(expenses) / len(expenses) if expenses else 0.0
        self.history.append(f"average_expense = {result}")
        return result

    def category_percentage(self, category_total: float, total_expenses: float) -> float:
        """Return a category total as a percentage of all expenses."""
        result = (category_total / total_expenses) * 100 if total_expenses else 0.0
        self.history.append(f"category_percentage = {result}")
        return result

    def savings_rate(self, income: float, expenses: float) -> float:
        """Return savings as a percentage of income."""
        result = ((income - expenses) / income) * 100 if income else 0.0
        self.history.append(f"savings_rate = {result}")
        return result

    # TODO: Implement forecast_month_end_spend(transactions, days_elapsed, days_in_month)
    # It should estimate month-end spending from current month-to-date expenses.
    def forecast_month_end_spend(self, transactions: List[Transaction], days_elapsed: int, days_in_month: int) -> float:
        """Estimate month-end expenses from spending to date."""
        current_expenses = self.total_expenses(transactions)
        if days_elapsed == 0:
            return 0.0
        result = (current_expenses / days_elapsed) * days_in_month
        self.history.append(f"forecast_month_end_spend = {result}")
        return result

    # TODO: Implement is_over_budget(monthly_budget, transactions)
    # It should return True when expenses exceed the monthly budget.
    def is_over_budget(self, monthly_budget: float, transactions: List[Transaction]) -> bool:
        """Return whether expenses exceed the monthly budget."""
        result = self.total_expenses(transactions) > monthly_budget
        self.history.append(f"is_over_budget({monthly_budget}) = {result}")
        return result

    def get_history(self) -> List[str]:
        """Return a copy of the calculation history."""
        return self.history.copy()


# Backward-compatible alias used by a few older demo prompts.
Calculator = BudgetCalculator
