from fastmcp import FastMCP
import sqlite3
import os
from pathlib import Path

mcp = FastMCP("SQLite MCP Server")

DB_PATH = Path(os.getenv("DB_PATH", "data/administradora 1.db"))


def get_connection():
    return sqlite3.connect(DB_PATH)


@mcp.tool()
def list_tables() -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [t[0] for t in cur.fetchall()]

    return {"tables": tables}


@mcp.tool()
def get_db_schema(table_name: str) -> dict:
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"PRAGMA table_info({table_name})")
    rows = cur.fetchall()

    return {
        "table": table_name,
        "columns": {row[1]: row[2] for row in rows}
    }
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8001
    )