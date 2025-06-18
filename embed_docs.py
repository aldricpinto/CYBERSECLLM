from app.services.embedding_service import EmbeddingService
import os

doc_paths = [
    "documents/USECASE 1.docx",
    "documents/USEcasetwo.docx"
]

embedder = EmbeddingService()
embedder.build_index_from_docs(doc_paths)

print("✅ FAISS vector index created and saved.")