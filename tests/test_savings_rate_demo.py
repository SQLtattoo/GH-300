import pytest

from calculator import BudgetCalculator


def test_savings_rate_with_zero_income_and_zero_expenses() -> None:
    assert BudgetCalculator().savings_rate(0.0, 0.0) == 0.0


def test_savings_rate_with_zero_income_and_positive_expenses() -> None:
    assert BudgetCalculator().savings_rate(0.0, 100.0) == 0.0


def test_savings_rate_with_positive_income() -> None:
    assert BudgetCalculator().savings_rate(1000.0, 800.0) == pytest.approx(20.0)