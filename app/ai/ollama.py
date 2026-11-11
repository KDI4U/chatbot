import requests

from app.core.config import settings
from app.ai.prompts import SYSTEM_PROMPT


class OllamaService:

    @staticmethod
    def generate_response(prompt: str) -> str:

        payload = {
            "model": settings.OLLAMA_MODEL,
            "system": SYSTEM_PROMPT,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "top_p": 0.9
            }
        }

        try:
            response = requests.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json=payload,
                timeout=120
            )

            response.raise_for_status()

            data = response.json()

            return data.get(
                "response",
                "Sorry, I couldn't generate a response."
            )

        except requests.exceptions.RequestException as ex:
            raise Exception(f"Ollama Error: {str(ex)}")