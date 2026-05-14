import sqlite3
from pathlib import Path
from typing import Generator
from app.config import settings


def get_connection() -> sqlite3.Connection:
    db_path = Path(settings.database_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
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
    db_path = Path(settings.database_path)
    if not db_path.exists():
        raise FileNotFoundError(f"No se encontró la base de datos SQLite: {db_path}")
    with get_connection() as db:
        tablas = {r["name"] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        requeridas = {"Usuario", "Balance_general", "Categoria", "Apartamento", "Gasto_apartamento"}
        faltantes = requeridas - tablas
        if faltantes:
            raise RuntimeError(f"Faltan tablas requeridas en SQLite: {', '.join(sorted(faltantes))}")
