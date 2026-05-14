from fastmcp import Client
from llm.client import get_llm
import json


client = Client("http://127.0.0.1:8001/mcp")


async def run_agent(file_path: str):

    llm = get_llm()

    messages = [
        {
            "role": "system",
            "content": """
Eres un AGENTE autónomo de transformación Excel → SQLite.

Tienes acceso a tools MCP:

TOOLS:
- read_excel(file_path)
- list_tables()
- get_schema(table_name)
- export_excel(data, output_name)
- insert_rows(table, rows)

REGLAS:
- SOLO puedes usar tools
- No inventes datos
- No inventes columnas
- Siempre basa todo en outputs de tools

REGLA CRÍTICA NUEVA:

- Debes detectar datos basura o de prueba
- Si el contenido del Excel parece texto aleatorio, test o frases sin estructura:
  → debes TERMINAR con error (action: finish)

EJEMPLOS DE BASURA:
- "hola", "como vas"
- "test", "prueba", "asdf"
- frases sin relación con datos reales de negocio

EJEMPLO DE DATOS VALIDOS:
- nombres, emails, direcciones, productos, registros estructurados


FLUJO IDEAL:
1. read_excel
2. list_tables
3. get_schema
4. transformar datos
5. export_excel

RESPONDE SIEMPRE EN JSON:

Si quieres usar tool:
{
  "action": "tool_name",
  "args": {}
}

Si quieres terminar:
{
  "action": "finish",
  "output_file": "ruta"
}
"""
        },
        {
            "role": "user",
            "content": f"Procesa este archivo: {file_path}"
        }
    ]

    async with client:

        for _ in range(15):

            response = llm.invoke(messages)

            content = response.content.strip()

            # 🔥 FIX WINDOWS PATHS
            content = content.replace("\\", "/")

            try:
                action_json = json.loads(content)
            except Exception:
                raise Exception(f"El LLM NO devolvió JSON válido:\n{content}")

            messages.append({
                "role": "assistant",
                "content": content
            })

            action = action_json.get("action")

            # -------------------------
            # FIN
            # -------------------------
            if action == "finish":
                return {
                    "status": "ok",
                    "file": action_json.get("output_file")
                }

            # -------------------------
            # TOOL CALL
            # -------------------------
            tool_args = action_json.get("args", {})

            try:
                tool_result = await client.call_tool(action, tool_args)
                tool_output = tool_result.content[0].text
            except Exception as e:
                tool_output = json.dumps({"error": str(e)})

            # 🔥 IMPORTANTÍSIMO: devolver contexto al LLM
            messages.append({
                "role": "user",
                "content": f"""
Resultado tool {action}:

{tool_output}

Decide siguiente acción.
"""
            })

    raise Exception("El agente no terminó en el límite de pasos")