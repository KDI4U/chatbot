import requests

from app.core.config import settings


class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str):

        response = requests.post(
            f"{settings.OLLAMA_URL}/api/embeddings",
            json={
                "model": settings.OLLAMA_EMBED_MODEL,
                "prompt": text
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["embedding"]


class EmbeddingService:

    @staticmethod
    def generate_embedding(text: str) -> list[float]:

        response = requests.post(
            f"{settings.OLLAMA_URL}/api/embeddings",
            json={
                "model": settings.OLLAMA_EMBED_MODEL,
                "prompt": text,
            },
            timeout=120,
        )

        response.raise_for_status()

        return response.json()["embedding"]