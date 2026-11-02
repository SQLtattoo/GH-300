from types import SimpleNamespace

import pytest

from data_table import (
    ColumnDefinition, DataTable, apply_search, get_paginated_data,
    process_table_data, sort_data,
)


@pytest.fixture
def columns() -> list[ColumnDefinition]:
    return [ColumnDefinition("name", "Name"), ColumnDefinition("age", "Age")]


@pytest.fixture
def rows() -> list[dict[str, object]]:
    return [{"name": "Charlie", "age": 30}, {"name": "Alice", "age": 20},
            {"name": "Bob", "age": 25}]


def test_table_pagination_and_metadata(rows, columns) -> None:
    table = DataTable(rows, columns, rows_per_page=2)
    assert table.get_columns() == columns
    assert table.get_current_page() == rows[:2]
    assert not table.is_empty()
    assert table.get_page_info() == {
        "current_page": 1, "total_pages": 2, "total_rows": 3,
        "start_row": 1, "end_row": 2, "has_prev": False, "has_next": True,
    }
    table.set_page(2)
    assert table.get_current_page() == rows[2:]
    assert table.get_page_info() == {
        "current_page": 2, "total_pages": 2, "total_rows": 3,
        "start_row": 3, "end_row": 3, "has_prev": True, "has_next": False,
    }
    for page in (0, 3):
        with pytest.raises(ValueError, match="Page must be between"):
            table.set_page(page)


def test_table_empty_state_and_invalid_page_size(columns) -> None:
    table = DataTable([], columns)
    assert table.is_empty()
    assert table.get_current_page() == []
    assert table.get_total_pages() == 1
    assert table.get_page_info() == {
        "current_page": 1, "total_pages": 1, "total_rows": 0,
        "start_row": 0, "end_row": 0, "has_prev": False, "has_next": False,
    }
    table.set_page(1)
    with pytest.raises(ValueError, match="rows_per_page"):
        DataTable([], columns, rows_per_page=0)


def test_search_sort_and_reset(rows, columns) -> None:
    original = [row.copy() for row in rows]
    table = DataTable(rows, columns, rows_per_page=1)
    table.set_page(2)
    table.search(" ALI ")
    assert table.get_search_query() == "ali"
    assert table.get_current_page() == [rows[1]]
    assert table.get_page_info()["current_page"] == 1
    table.search("not found")
    assert table.is_empty()
    table.search("  ")
    assert table.get_total_rows() == 3
    table.sort("age", ascending=False)
    assert table.get_current_page() == [rows[0]]
    assert table.get_sort_state() == {"column": "age", "ascending": False}
    table.sort("name")
    assert table.get_current_page() == [rows[1]]
    table.reset()
    assert table.get_current_page() == rows[:1]
    assert table.get_search_query() == ""
    assert table.get_sort_state() == {"column": None, "ascending": True}
    assert rows == original


def test_sort_rejects_unknown_and_unsortable_columns(rows) -> None:
    table = DataTable(rows, [ColumnDefinition("name", "Name", sortable=False)])
    with pytest.raises(ValueError, match="not found"):
        table.sort("missing")
    with pytest.raises(ValueError, match="not sortable"):
        table.sort("name")


def test_object_rows_missing_values_and_formatters(columns) -> None:
    item = SimpleNamespace(name="Alice", age=20)
    table = DataTable([item, SimpleNamespace()], columns)
    table.search("20")
    assert table.get_current_page() == [item]
    assert table.format_cell(item, columns[0]) == "Alice"
    assert table.format_cell(item, ColumnDefinition("missing", "Missing")) == ""
    assert table.format_cell(item, ColumnDefinition("age", "Age", formatter=lambda value: f"{value} years")) == "20 years"


def test_pure_search_and_sort_support_objects_and_missing_values(columns) -> None:
    objects = [SimpleNamespace(name="Bob"), SimpleNamespace(name="Alice"), SimpleNamespace()]
    assert apply_search(objects, columns, " ALI ") == [objects[1]]
    assert apply_search(objects, columns, "nothing") == []
    assert apply_search(objects, columns, " ") == objects
    assert sort_data(objects, "name") == [objects[2], objects[1], objects[0]]
    rows = [{"name": "Bob"}, {"name": "Alice"}, {}]
    original = rows.copy()
    assert sort_data(rows, "name", ascending=False) == [rows[0], rows[1], rows[2]]
    assert rows == original


@pytest.mark.parametrize("page,size", [(0, 2), (1, 0), (1, -1)])
def test_pure_pagination_rejects_invalid_input(page: int, size: int) -> None:
    with pytest.raises(ValueError):
        get_paginated_data([1, 2, 3], page, size)


def test_pure_pagination_slices_without_mutation() -> None:
    rows = [1, 2, 3]
    assert get_paginated_data(rows, 2, 2) == [3]
    assert get_paginated_data(rows, 3, 2) == []
    assert rows == [1, 2, 3]


def test_combined_processing_and_page_clamping(rows, columns) -> None:
    result = process_table_data(rows, columns, search_query="a", sort_column="age",
                                sort_ascending=False, page=99, rows_per_page=1)
    assert result == {
        "rows": [rows[1]], "total_rows": 2, "total_pages": 2,
        "current_page": 2, "has_prev": True, "has_next": False,
        "start_row": 2, "end_row": 2,
    }
    assert process_table_data(rows, columns, page=0)["current_page"] == 1
    assert process_table_data([], columns, page=9) == {
        "rows": [], "total_rows": 0, "total_pages": 1, "current_page": 1,
        "has_prev": False, "has_next": False, "start_row": 0, "end_row": 0,
    }