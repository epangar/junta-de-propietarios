from fastmcp import Client
import json
import pandas as pd
import numpy as np
import math

client = Client("http://127.0.0.1:8001/mcp")


# ----------------------------
# SAFE JSON CONVERTER (CLAVE)
# ----------------------------
def safe_json(obj):
    if isinstance(obj, dict):
        return {k: safe_json(v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [safe_json(v) for v in obj]

    if isinstance(obj, pd.Timestamp):
        return obj.isoformat()

    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)

    if isinstance(obj, (np.floating, np.float64)):
        if math.isnan(obj):
            return None
        return float(obj)

    if isinstance(obj, float) and math.isnan(obj):
        return None

    return obj


async def run_agent(sheets):

    async with client:

        # ------------------------
        # BD STRUCTURE
        # ------------------------
        tables_result = await client.call_tool("list_tables", {})
        tables = json.loads(tables_result.content[0].text)["tables"]

        database_structure = {}

        for table in tables:
            schema_result = await client.call_tool(
                "get_db_schema",
                {"table_name": table}
            )

            schema = json.loads(schema_result.content[0].text)

            database_structure[table] = {
                "columns": schema["columns"]
            }

        # ------------------------
        # EXCEL STRUCTURE
        # ------------------------
        excel_structure = {}

        for sheet_name, df in sheets.items():

            sample_rows = df.head(5).to_dict(orient="records")
            sample_rows = safe_json(sample_rows)

            excel_structure[sheet_name] = {
                "columns": list(df.columns),
                "sample_data": sample_rows
            }

        # ------------------------
        # PROMPT LLM (opcional pero útil)
        # ------------------------
        prompt = f"""
Eres un analizador de estructuras de datos.

Tienes:

1. ESTRUCTURA EXCEL:
{json.dumps(excel_structure, indent=2, ensure_ascii=False)}

2. ESTRUCTURA BASE DE DATOS:
{json.dumps(database_structure, indent=2, ensure_ascii=False)}

TAREA:
- Describe si puedes leer correctamente el Excel
- Describe si puedes leer correctamente la BD
- No hagas validaciones
- No compares
- Solo explica estructuras detectadas

RESPONDE EN JSON:
{{
  "excel_ok": true,
  "db_ok": true,
  "resumen_excel": "",
  "resumen_db": ""
}}
"""

        response = await client.call_tool("list_tables", {})  # keep alive
        # (puedes quitar esto si quieres)

        # aquí asumo que tienes LLM externo:
        # llm = get_llm()
        # result = llm.invoke(prompt)

        # 🔥 SIN LLM fallback (estructura pura)
        result = {
            "excel_structure": excel_structure,
            "database_structure": database_structure
        }

        return result