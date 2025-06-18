# app/services/rag_service.py

import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
from app.services.parser_service import parse_file
import requests
from pathlib import Path

FAISS_INDEX_PATH = "vectorstore/faiss_index.pkl"

# Load embedder
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_relevant_chunks(query: str, top_k=3):
    with open(FAISS_INDEX_PATH, "rb") as f:
        index, metadata = pickle.load(f)

    query_vec = model.encode([query]).astype("float32")
    distances, indices = index.search(query_vec, top_k)

    return [metadata[i] for i in indices[0]]

def ask_mistral(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",  # Ollama's API
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json().get("response", "[No response from Mistral]")

def analyze_artifact(file: Path) -> str:
    parsed_text = parse_file(file)
    if "Unsupported" in parsed_text:
        return parsed_text

    retrieved_chunks = retrieve_relevant_chunks(parsed_text)

    prompt = f"""
        You are a digital forensic analyst.

        Here is forensic event data extracted from a JSON-LD file uploaded by the user:
        ---
        {parsed_text}
        ---

        Here are known forensic patterns from previous cases this is a knowledge-base for you. 
        As this is a knowledge-base use these only as general references, not as facts in your explanation:
        ---
        {''.join(retrieved_chunks)}
        ---

        Now, can you identify any anomalies in the json-ld file uploaded by the user is yes
        Explain clearly, and do not mention anything from the knowledge-base just stick to using the knowledge base as reference for you inferencing.
        And I want the ouput to look like if Anomaly is present:
        Anomaly Detected : True
        Description: < here write about the anomaly you detected and why you think its an anomaly >
        And I want the ouput to look like if Anomaly is not present:
        Anomaly Detected : False
        Description: No Anomalies detected !
        And again it is very important that you stick to this template for you response part and do not mention anything else especially nothing
        from the knowledge-base
        
        """
    return ask_mistral(prompt)