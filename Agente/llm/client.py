from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5")


_llm_instance = None


def get_llm():
    global _llm_instance

    if _llm_instance is None:

        custom_headers = {
            "origin": "research",
            "origin-detail": "reskilling",
            "provider": "AzureOpenAI",
        }

        _llm_instance = ChatOpenAI(
            model=MODEL_NAME,
            api_key=API_KEY,
            base_url=API_BASE_URL,
            default_headers=custom_headers,
            temperature=0,
        )

    return _llm_instance