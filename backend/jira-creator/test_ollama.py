import httpx
import json
import sys

OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama2:latest"

SYSTEM_PROMPT = (
    "Eres un asistente experto en gestión de proyectos. "
    "A partir del texto que recibas, debes extraer y estructurar "
    "una o varias tarjetas de Jira en formato JSON. "
    "Devuelve ÚNICAMENTE un JSON válido con la siguiente estructura:\n"
    "{\n"
    '  "issues": [\n'
    "    {\n"
    '      "summary": "Título de la tarea",\n'
    '      "description": "Descripción detallada",\n'
    '      "issue_type": "Task|Bug|Story|Epic",\n'
    '      "priority": "Highest|High|Medium|Low|Lowest",\n'
    '      "labels": ["label1", "label2"]\n'
    "    }\n"
    "  ]\n"
    "}\n"
    "No incluyas texto adicional fuera del JSON."
)

USER_TEXT = "Necesitamos implementar login con OAuth2 y corregir un bug en el formulario de registro."

def check_ollama_running():
    try:
        with httpx.Client(timeout=5.0) as client:
            r = client.get(f"{OLLAMA_URL}/api/tags")
            r.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Ollama no está respondiendo en {OLLAMA_URL}: {e}")
        return False

def send_test_request():
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 250
        },
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEXT}
        ]
    }

    print(f"📤 Enviando petición a {OLLAMA_URL}/api/chat con modelo {MODEL_NAME}...")
    try:
        with httpx.Client(timeout=300.0) as client:
            r = client.post(f"{OLLAMA_URL}/api/chat", headers={"Content-Type": "application/json"}, json=payload)
            r.raise_for_status()
    except httpx.RequestError as e:
        print(f"❌ Error de conexión: {e}")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
        sys.exit(1)

    data = r.json()
    print("\n✅ Respuesta completa:")
    print(json.dumps(data, indent=2))

    if "message" in data and "content" in data["message"]:
        print("\n📄 Contenido generado por Llama2:")
        print(data["message"]["content"])

if __name__ == "__main__":
    if not check_ollama_running():
        print("⚠️ Inicia Ollama con: ollama serve")
        sys.exit(1)

    send_test_request()
