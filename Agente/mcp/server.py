from fastmcp import FastMCP
import sqlite3
import pandas as pd
from pathlib import Path
import re

mcp = FastMCP("Excel Agent MCP")

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "administradora.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn



NOISE_WORDS = {
    "hola", "test", "prueba", "asdf", "asdfasdf",
    "como vas", "ok", "lorem", "ipsum"
}


def is_valid_cell(value) -> bool:
    if value is None:
        return False

    if not isinstance(value, str):
        return True  # números/fechas se aceptan

    v = value.strip().lower()

    # demasiado corto
    if len(v) < 3:
        return False

    # ruido típico
    if v in NOISE_WORDS:
        return False

    # solo letras repetidas sin sentido
    if re.fullmatch(r"(.)\1{3,}", v):
        return False

    return True


def is_valid_row(row: dict) -> bool:
    values = list(row.values())

    valid_cells = sum(is_valid_cell(v) for v in values)
    total_cells = len(values)

    # regla fuerte: al menos 60% deben ser “datos válidos”
    return valid_cells / max(total_cells, 1) >= 0.6


@mcp.tool()
def read_excel(file_path: str):

    try:
        xls = pd.read_excel(file_path, sheet_name=None)

        result = {}

        total_rows = 0
        total_sheets = 0

        for name, df in xls.items():
            df = df.where(pd.notnull(df), None)

            rows_count = len(df)
            total_rows += rows_count
            total_sheets += 1

            result[name] = {
                "columns": list(df.columns),
                "rows": df.head(20).to_dict(orient="records"),
                "row_count": rows_count
            }

        # 🔴 VALIDACIÓN CRÍTICA: EXCEL VACÍO
        if total_sheets == 0 or total_rows == 0:
            return {
                "status": "error",
                "message": "El Excel está vacío (no hay datos en ninguna hoja)",
                "tables_found": total_sheets,
                "rows_found": total_rows
            }

        return {
            "status": "success",
            "sheets": result,
            "tables_found": total_sheets,
            "rows_found": total_rows
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error leyendo Excel: {str(e)}"
        }


@mcp.tool()
def list_tables():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]

    conn.close()
    return {"tables": tables}


@mcp.tool()
def get_schema(table_name: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table_name})")
    rows = cur.fetchall()

    conn.close()

    return {
        "table": table_name,
        "columns": {r[1]: r[2] for r in rows}
    }


@mcp.tool()
def insert_rows(table: str, rows: list):

    if not rows:
        return {"status": "error", "message": "empty rows"}

    conn = get_conn()
    cur = conn.cursor()

    try:
        columns = list(rows[0].keys())

        clean_rows = []
        rejected_rows = []

        # -------------------------
        # 1. FILTRO SEMÁNTICO
        # -------------------------
        for row in rows:
            if is_valid_row(row):
                clean_rows.append(row)
            else:
                rejected_rows.append(row)

        if len(clean_rows) == 0:
            return {
                "status": "error",
                "message": "Todos los datos fueron rechazados (posible basura o test data)",
                "rejected": rejected_rows
            }

        # -------------------------
        # 2. DUPLICADOS EN EXCEL
        # -------------------------
        seen = set()
        final_clean = []
        duplicates_input = []

        for row in clean_rows:
            key = tuple(row.get(col) for col in columns)

            if key in seen:
                duplicates_input.append(row)
            else:
                seen.add(key)
                final_clean.append(row)

        if duplicates_input:
            return {
                "status": "error",
                "message": "Duplicados dentro del input",
                "duplicates": duplicates_input
            }

        # -------------------------
        # 3. DUPLICADOS EN BD
        # -------------------------
        placeholders = ",".join(["?"] * len(columns))
        columns_sql = ",".join(columns)

        cur.execute(f"SELECT {columns_sql} FROM {table}")
        existing_rows = set(cur.fetchall())

        final_rows = []
        duplicates_db = []

        for row in final_clean:
            key = tuple(row.get(col) for col in columns)

            if key in existing_rows:
                duplicates_db.append(row)
            else:
                final_rows.append(row)

        if duplicates_db:
            return {
                "status": "error",
                "message": "Datos ya existentes en BD",
                "duplicates": duplicates_db
            }

        # -------------------------
        # 4. INSERT
        # -------------------------
        query = f"""
        INSERT INTO {table} ({columns_sql})
        VALUES ({placeholders})
        """

        values = [
            tuple(row.get(col) for col in columns)
            for row in final_rows
        ]

        cur.executemany(query, values)
        conn.commit()

        return {
            "status": "success",
            "inserted": len(values),
            "rejected_rows": len(rejected_rows)
        }

    except Exception as e:
        conn.rollback()
        return {"status": "error", "error": str(e)}

    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001
    )