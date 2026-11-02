"""Budget Buddy demo application entry point."""

from calculator import BudgetCalculator
from data_processor import TransactionProcessor
from data_table import ColumnDefinition, DataTable
from file_handler import BudgetFileHandler
from logger import logger


def format_currency(value: object) -> str:
    """Format a numeric value as currency."""
    return f"${float(value):,.2f}"


def build_report(monthly_budget: float, transactions: list[dict[str, object]]) -> dict[str, object]:
    """Build a simple budget report from transactions."""
    calculator = BudgetCalculator()
    processor = TransactionProcessor()

    expenses = calculator.total_expenses(transactions)
    income = calculator.total_income(transactions)
    category_totals = processor.group_expenses_by_category(transactions)
    top_merchants = processor.top_merchants(transactions)

    return {
        "monthly_budget": monthly_budget,
        "income": income,
        "expenses": expenses,
        "remaining_budget": calculator.remaining_budget(monthly_budget, transactions),
        "net_cash_flow": calculator.net_cash_flow(transactions),
        "savings_rate": calculator.savings_rate(income, expenses),
        "largest_expense": processor.largest_expense(transactions),
        "category_totals": category_totals,
        "top_merchants": top_merchants,
    }


def show_transactions(transactions: list[dict[str, object]]) -> None:
    """Log a small transaction table."""
    columns = [
        ColumnDefinition("date", "Date"),
        ColumnDefinition("merchant", "Merchant"),
        ColumnDefinition("category", "Category"),
        ColumnDefinition("amount", "Amount", formatter=format_currency),
        ColumnDefinition("type", "Type"),
    ]
    table = DataTable(transactions, columns, rows_per_page=6)

    logger.info("Recent transactions")
    logger.info("Date       | Merchant             | Category      | Amount     | Type")
    logger.info("-" * 72)
    for item in table.get_current_page():
        logger.info(
            f"{item['date']} | {item['merchant']:<20} | {item['category']:<13} | "
            f"{format_currency(item['amount']):>10} | {item['type']}"
        )


def show_top_merchants(merchants: list[dict[str, object]]) -> None:
    """Log the highest-spend merchants as a compact table."""
    logger.info("Top merchants by spend")
    if not merchants:
        logger.info("No expense transactions.")
        return

    columns = [
        ColumnDefinition("merchant", "Merchant"),
        ColumnDefinition("amount", "Amount", formatter=format_currency),
    ]
    table = DataTable(merchants, columns, rows_per_page=5)
    logger.info("Merchant             | Amount")
    logger.info("----------------------|----------")
    for item in table.get_current_page():
        logger.info(f"{item['merchant']:<20} | {format_currency(item['amount']):>8}")


def main() -> None:
    """Run the Budget Buddy demo app."""
    monthly_budget = 3200.00
    handler = BudgetFileHandler("data")
    transactions = handler.read_transactions_csv("sample_transactions.csv")
    report = build_report(monthly_budget, transactions)

    logger.info("Budget Buddy - GitHub Copilot Demo App")
    logger.info("=" * 48)
    show_transactions(transactions)
    logger.info("=" * 48)
    logger.info(f"Monthly budget: {format_currency(report['monthly_budget'])}")
    logger.info(f"Income: {format_currency(report['income'])}")
    logger.info(f"Expenses: {format_currency(report['expenses'])}")
    logger.info(f"Remaining budget: {format_currency(report['remaining_budget'])}")
    logger.info(f"Net cash flow: {format_currency(report['net_cash_flow'])}")
    logger.info(f"Savings rate: {report['savings_rate']:.1f}%")
    logger.info(f"Largest expense: {report['largest_expense']}")
    logger.info(f"Category totals: {report['category_totals']}")
    show_top_merchants(report["top_merchants"])
    logger.info("Demo-start app completed. Now use Copilot to harden it.")


if __name__ == "__main__":
    main()