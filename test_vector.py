# from app.rag.vector_store import VectorStore

# db = VectorStore()

# print("Documents:", db.count())


from app.rag.vector_store import VectorStore

vector_store = VectorStore()

print("=" * 50)
print("Total Documents in ChromaDB :", vector_store.count())
print("=" * 50)