"""
Financial calculation helpers for the Budget Buddy demo app.

This module is intentionally starter-quality for GitHub Copilot demos. Some
methods work on the happy path, while selected edge cases are left for
learners to fix with Copilot.
"""

from typing import Dict, List


Transaction = Dict[str, object]


class BudgetCalculator:

    def __init__(self) -> None:
        """Initialize an empty calculation history."""
        self.history: List[str] = []

    def total_income(self, transactions: List[Transaction]) -> float:
        """Return the sum of income transaction amounts."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "income")
        self.history.append(f"total_income = {total}")
        return total

    def total_expenses(self, transactions: List[Transaction]) -> float:
        """Return the sum of expense transaction amounts."""
        total = sum(float(item["amount"]) for item in transactions if item.get("type") == "expense")
        self.history.append(f"total_expenses = {total}")
        return total

    def net_cash_flow(self, transactions: List[Transaction]) -> float:
        """Return total income minus total expenses."""
        result = self.total_income(transactions) - self.total_expenses(transactions)
        self.history.append(f"net_cash_flow = {result}")
        return result

    def remaining_budget(self, monthly_budget: float, transactions: List[Transaction]) -> float:
        """Return the monthly budget minus total expenses."""
        result = monthly_budget - self.total_expenses(transactions)
        self.history.append(f"remaining_budget({monthly_budget}) = {result}")
        return result

    def average_expense(self, transactions: List[Transaction]) -> float:
        """Return mean expense amount; raise ZeroDivisionError if no expenses exist."""
        expenses = [float(item["amount"]) for item in transactions if item.get("type") == "expense"]
        result = sum(expenses) / len(expenses)
        self.history.append(f"average_expense = {result}")
        return result

    def category_percentage(self, category_total: float, total_expenses: float) -> float:
        """Return category share as a percentage; raise ZeroDivisionError for a zero total."""
        result = (category_total / total_expenses) * 100
        self.history.append(f"category_percentage = {result}")
        return result

    def savings_rate(self, income: float, expenses: float) -> float:
        """Return savings as a percentage of income, or 0.0 for zero income."""
        result = 0.0 if income == 0 else ((income - expenses) / income) * 100
        self.history.append(f"savings_rate = {result}")
        return result

    def forecast_month_end_spend(
        self, transactions: List[Transaction], days_elapsed: int, days_in_month: int
    ) -> float:
        """Project month-to-date expenses over a valid elapsed day range."""
        if days_in_month <= 0 or not 1 <= days_elapsed <= days_in_month:
            raise ValueError("Days must satisfy 1 <= days_elapsed <= days_in_month")
        result = self.total_expenses(transactions) / days_elapsed * days_in_month
        self.history.append(f"forecast_month_end_spend = {result}")
        return result

    def is_over_budget(self, monthly_budget: float, transactions: List[Transaction]) -> bool:
        """Return whether expenses strictly exceed the monthly budget."""
        result = self.total_expenses(transactions) > monthly_budget
        self.history.append(f"is_over_budget({monthly_budget}) = {result}")
        return result

    def get_history(self) -> List[str]:
        """Return a copy of the recorded calculation history."""
        return self.history.copy()


# Backward-compatible alias used by a few older demo prompts.
Calculator = BudgetCalculator
