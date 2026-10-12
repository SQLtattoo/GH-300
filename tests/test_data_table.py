"""Tests for table searching, sorting, pagination, and formatting."""

from dataclasses import dataclass

import pytest

from data_table import (
    ColumnDefinition,
    DataTable,
    apply_search,
    get_paginated_data,
    process_table_data,
    sort_data,
)


@pytest.fixture
def table_rows():
    """Return rows suitable for all table transformations."""
    return [
        {"name": "Alice", "age": 30, "score": 85},
        {"name": "Bob", "age": 25, "score": 92},
        {"name": "Charlie", "age": 35, "score": None},
    ]


@pytest.fixture
def table_columns():
    """Return sortable and non-sortable column definitions."""
    return [
        ColumnDefinition("name", "Name"),
        ColumnDefinition("age", "Age"),
        ColumnDefinition("score", "Score", sortable=False),
    ]


def test_rows_per_page_must_be_positive(table_columns):
    """Reject invalid page sizes."""
    with pytest.raises(ValueError, match="at least 1"):
        DataTable([], table_columns, rows_per_page=0)


def test_search_is_case_insensitive_and_can_be_reset(table_rows, table_columns):
    """Filter across columns, reset pagination, and restore all rows."""
    table = DataTable(table_rows, table_columns, rows_per_page=1)
    table.set_page(2)

    table.search("  ALI ")
    assert table.get_current_page() == [table_rows[0]]
    assert table.get_search_query() == "ali"
    assert table.get_page_info()["current_page"] == 1

    table.search("")
    assert table.get_total_rows() == 3


def test_table_supports_object_attributes(table_columns):
    """Read searchable values from objects as well as dictionaries."""
    @dataclass
    class Person:
        name: str
        age: int
        score: int

    person = Person("Dana", 40, 99)
    table = DataTable([person], table_columns)
    table.search("dana")

    assert table.get_current_page() == [person]
    assert table.format_cell(person, table_columns[1]) == "40"


def test_sort_validates_columns_and_sortability(table_rows, table_columns):
    """Reject unknown and explicitly non-sortable columns."""
    table = DataTable(table_rows, table_columns)

    with pytest.raises(ValueError, match="not found"):
        table.sort("missing")
    with pytest.raises(ValueError, match="not sortable"):
        table.sort("score")


def test_sort_tracks_direction_and_resets_page(table_rows, table_columns):
    """Sort both directions while recording the active sort state."""
    table = DataTable(table_rows, table_columns, rows_per_page=2)
    table.set_page(2)

    table.sort("age", ascending=False)

    assert [row["name"] for row in table.get_current_page()] == ["Charlie", "Alice"]
    assert table.get_sort_state() == {"column": "age", "ascending": False}
    assert table.get_page_info()["current_page"] == 1


def test_pagination_reports_boundaries(table_rows, table_columns):
    """Return the correct page slice and navigation metadata."""
    table = DataTable(table_rows, table_columns, rows_per_page=2)
    table.set_page(2)

    assert table.get_current_page() == [table_rows[2]]
    assert table.get_page_info() == {
        "current_page": 2,
        "total_pages": 2,
        "total_rows": 3,
        "start_row": 3,
        "end_row": 3,
        "has_prev": True,
        "has_next": False,
    }

    with pytest.raises(ValueError, match="between 1 and 2"):
        table.set_page(0)
    with pytest.raises(ValueError, match="between 1 and 2"):
        table.set_page(3)


def test_empty_table_and_cell_formatting(table_columns):
    """Describe empty data and format nullable or customized values."""
    table = DataTable([], table_columns)
    formatted_column = ColumnDefinition("score", "Score", formatter=lambda value: f"{value}%")

    assert table.is_empty() is True
    assert table.get_total_pages() == 1
    assert table.get_page_info()["start_row"] == 0
    assert table.format_cell({"score": None}, table_columns[2]) == ""
    assert table.format_cell({"score": 85}, formatted_column) == "85%"
    assert table.get_columns() == table_columns


def test_reset_restores_initial_state(table_rows, table_columns):
    """Clear search, sorting, and pagination state."""
    table = DataTable(table_rows, table_columns, rows_per_page=1)
    table.search("alice")
    table.sort("name", ascending=False)
    table.reset()

    assert table.get_current_page() == [table_rows[0]]
    assert table.get_search_query() == ""
    assert table.get_sort_state() == {"column": None, "ascending": True}


def test_pure_search_and_sort_do_not_mutate_input(table_rows, table_columns):
    """Apply standalone transformations to dictionaries and objects."""
    original = table_rows.copy()

    assert apply_search(table_rows, table_columns, "LI") == [table_rows[0], table_rows[2]]
    assert apply_search(table_rows, table_columns, "  ") is table_rows
    assert [row["name"] for row in sort_data(table_rows, "age", False)] == [
        "Charlie",
        "Alice",
        "Bob",
    ]
    assert table_rows == original


@pytest.mark.parametrize(
    ("page", "rows_per_page", "message"),
    [(0, 2, "Page must"), (1, 0, "rows_per_page must")],
)
def test_standalone_pagination_validates_arguments(table_rows, page, rows_per_page, message):
    """Reject invalid standalone pagination arguments."""
    with pytest.raises(ValueError, match=message):
        get_paginated_data(table_rows, page, rows_per_page)


def test_process_table_data_combines_transformations(table_rows, table_columns):
    """Search, sort, paginate, and report metadata in one call."""
    result = process_table_data(
        table_rows,
        table_columns,
        search_query="li",
        sort_column="age",
        sort_ascending=False,
        page=9,
        rows_per_page=1,
    )

    assert result == {
        "rows": [table_rows[0]],
        "total_rows": 2,
        "total_pages": 2,
        "current_page": 2,
        "has_prev": True,
        "has_next": False,
        "start_row": 2,
        "end_row": 2,
    }


def test_process_table_data_handles_empty_data_and_low_page(table_columns):
    """Clamp low page numbers and return coherent empty metadata."""
    result = process_table_data([], table_columns, page=0, rows_per_page=5)

    assert result["rows"] == []
    assert result["current_page"] == 1
    assert result["total_pages"] == 1
    assert result["start_row"] == 0
    assert result["end_row"] == 0