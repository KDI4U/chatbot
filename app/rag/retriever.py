from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class Retriever:

    @staticmethod
    def search(question: str, top_k: int = 8):

        vector_store = VectorStore()

        embedding = EmbeddingService.generate_embedding(question)

        results = vector_store.search(
            embedding=embedding,
            top_k=top_k
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        filtered_docs = []

        for doc, distance in zip(documents, distances):

            # Lower distance = better match
            if distance <= 1.2:   # <-- tune this after testing
                filtered_docs.append(doc)

        # If no relevant documents found, return EMPTY LIST
        return filtered_docs