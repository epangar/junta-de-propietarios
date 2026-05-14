# Junta de Propietarios

Proyecto para gestionar la junta de propietarios de una comunidad.

Un sistema autónomo basado en agentes que transforma archivos Excel en datos estructurados dentro de una base de datos SQLite usando un LLM y herramientas MCP (Model Context Protocol).

---

# 🚀 Qué hace este proyecto

- 📁 Sube archivos Excel vía API
- 🤖 Un agente LLM analiza el contenido
- 🧠 Decide acciones usando tools MCP
- 🧹 Filtra automáticamente datos basura o de prueba
- 🗄️ Inserta datos válidos en SQLite
- 🚫 Evita duplicados y datos inconsistentes

---

# 🏗️ Arquitectura

Excel File → FastAPI → Agent (LLM loop) → MCP Tools Server → SQLite

---

# ⚙️ Tecnologías

- FastAPI
- FastMCP
- LLM (OpenAI / compatible)
- Pandas
- SQLite
- Python 3.10+

---

# 📂 Estructura

project/
├── main.py
├── agent/
│   └── agent.py
├── mcp/
│   └── server.py
├── llm/
│   └── client.py
├── data/
│   └── administradora.db
├── requirements.txt
└── README.md

---

# 🚀 Instalación

# 1. Crear entorno
python -m venv venv
source venv/bin/activate
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt


# 3. ▶️ Ejecución
1. Levantar MCP Server
python mcp_server/tools.py

http://127.0.0.1:8001/mcp

2. Levantar API
uvicorn main:app --reload

http://127.0.0.1:8000

📤 Endpoint

POST /upload-file

Form-data:
file → archivo .xlsx


📥 Respuesta
{
  "status": "ok",
  "file": "ruta_del_resultado"
}

🧠 Cómo funciona el agente
Lee Excel (read_excel)
Analiza estructura
LLM decide acción
Ejecuta tools MCP
Filtra datos basura automáticamente
Inserta en SQLite


🧹 Limpieza de datos

❌ Se rechaza automáticamente:

“hola”
“test”
“asdf”
frases sin estructura
datos conversacionales

🛡️ Validaciones

✔ Detección de basura
✔ Filtro semántico
✔ Validación estructural
✔ Protección contra datos inválidos