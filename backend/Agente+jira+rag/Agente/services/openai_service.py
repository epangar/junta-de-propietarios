import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from config import Settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, settings: Settings):
        # Guardar settings en la instancia antes de usarlo
        self.settings = settings

        # Obtener API key (puede ser str o SecretStr)
        api_key_value = (
            self.settings.OPENAI_API_KEY.get_secret_value()
            if hasattr(self.settings.OPENAI_API_KEY, "get_secret_value")
            else self.settings.OPENAI_API_KEY
        )

        if not api_key_value:
            raise ValueError("OPENAI_API_KEY está vacío. Configúralo en config.py.")

        # Crear el modelo usando LangChain ChatOpenAI
        self.model = ChatOpenAI(
            api_key=api_key_value,
            model=self.settings.OPENAI_MODEL,
            base_url=self.settings.OPENAI_BASE_URL,
            default_headers={
                "origin": "research",
                "origin-detail": "reskilling",
                "provider": "AzureOpenAI"
            },
            temperature=self.settings.OPENAI_TEMPERATURE
        )

    async def generate_jira_issues(self, text: str) -> tuple[list[dict], str]:
        """
        Envía el texto al modelo y devuelve lista de dicts con las tarjetas Jira.
        """
        messages = [
            SystemMessage(content=self.settings.OPENAI_SYSTEM_PROMPT),
            HumanMessage(content=text)
        ]

        logger.info("Enviando petición al modelo %s", self.settings.OPENAI_MODEL)

        # Invocar el modelo
        response = self.model.invoke(messages)
        raw_content = response.content

        logger.debug("Respuesta cruda: %s", raw_content)

        # Extraer solo el JSON
        raw_content_clean = self._extract_json(raw_content)

        try:
            parsed = json.loads(raw_content_clean)
            issues = parsed.get("issues", [])
        except json.JSONDecodeError as exc:
            logger.error("El modelo no devolvió un JSON válido: %s", exc)
            raise ValueError(f"Respuesta inválida: {raw_content}") from exc

        return issues, raw_content

    def _extract_json(self, text: str) -> str:
        """
        Extrae el bloque JSON de la respuesta aunque haya texto extra.
        """
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end > start:
            return text[start:end]
        return text
    