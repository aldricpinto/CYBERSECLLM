import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

# Load index and metadata
with open("vectorstore/faiss_index.pkl", "rb") as f:
    index, metadata = pickle.load(f)

# Load the same embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Sample query
query = "Can you find any timestamp manipulation or time-stomping behavior?"

# Encode query to match dimensions
query_vector = model.encode([query]).astype("float32")

# Search the index (top 3 results)
k = 3
distances, indices = index.search(query_vector, k)

# Show results
print(f"\n🔍 Top {k} results for query: \"{query}\"")
for i, idx in enumerate(indices[0]):
    print(f"\nResult {i+1}:")
    print(f"Distance Score: {distances[0][i]}")
    print(f"Chunk:\n{metadata[idx]}")
