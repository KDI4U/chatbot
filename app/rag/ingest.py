import uuid

from app.rag.loader import DocumentLoader
from app.rag.chunker import TextChunker
from app.rag.embeddings import EmbeddingService
from app.rag.vector_store import VectorStore


class DocumentIngestor:

    @staticmethod
    def ingest(file_path: str):

        vector_store = VectorStore()

        print("Loading PDF...")
        documents = DocumentLoader.load_pdf(file_path)

        print(f"Pages: {len(documents)}")

        print("Splitting document...")
        chunks = TextChunker.split(documents)

        print(f"Chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks, start=1):

            print(f"Embedding chunk {index}/{len(chunks)}")

            embedding = EmbeddingService.generate_embedding(
                chunk.page_content
            )

            vector_store.add_document(
                doc_id=str(uuid.uuid4()),
                text=chunk.page_content,
                embedding=embedding,
                metadata={
                    "source": chunk.metadata.get("source", ""),
                    "page": chunk.metadata.get("page", 0),
                },
            )

        print("✅ Document indexed successfully.")