import chromadb


class VectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="vector_db"
        )

        self.collection = self.client.get_or_create_collection(
            name="bswan_library"
        )

    def add_document(
        self,
        doc_id: str,
        text: str,
        embedding: list[float],
        metadata: dict,
    ):
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 8,
    ):

        return self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

    def count(self):
        return self.collection.count()