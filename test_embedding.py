from app.rag.embeddings import EmbeddingService

embedding = EmbeddingService.generate_embedding(
    "What is BSWAN?"
)

print(type(embedding))
print(len(embedding))
print(embedding[:5])