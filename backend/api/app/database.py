import sqlite3
from typing import Generator
from app.config import settings

DB_PATH = settings.database_path

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

def run_startup_checks() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"No se encontró la base de datos: {DB_PATH}")
    with get_connection() as conn:
        tablas = {r["name"] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        requeridas = {"Usuario", "Balance_general", "Apartamento", "Gasto_apartamento"}
        faltantes = requeridas - tablas
        if faltantes:
            raise RuntimeError(f"Faltan tablas requeridas: {', '.join(sorted(faltantes))}")
