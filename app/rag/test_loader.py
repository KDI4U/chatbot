from app.rag.loader import DocumentLoader
from app.rag.chunker import TextChunker


docs = DocumentLoader.load_pdf(
    "documents/sample.pdf"
)

print(f"Pages : {len(docs)}")

chunks = TextChunker.split(docs)

print(f"Chunks : {len(chunks)}")

print("-" * 80)

print(chunks[0].page_content)

from app.rag.vector_store import VectorStore

db = VectorStore()

print(db.collection.count())