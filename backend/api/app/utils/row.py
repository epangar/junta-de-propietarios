from sqlite3 import Row
from typing import Any


def row_to_dict(row: Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


def rows_to_list(rows: list[Row]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]
