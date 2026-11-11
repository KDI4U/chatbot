from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class Retriever:

    @staticmethod
    def search(question: str, top_k: int = 5):

        vector_store = VectorStore()

        embedding = EmbeddingService.generate_embedding(question)

        results = vector_store.search(
            embedding=embedding,
            top_k=top_k
        )

        return results.get("documents", [[]])[0]