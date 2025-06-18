import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

class EmbeddingService:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='vectorstore/faiss_index.pkl'):
        self.embedder = SentenceTransformer(model_name)
        self.index_path = index_path
        
        # Spliting long documents into manageable overlapping chunks (for context continuity)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=64,
        )
        
        # here the 384 dimensions will be the output of the MiniLM model per text chunk
        # MiniLM model works as a SentenceTransformer (used for embedding)
        
        # FAISS index will store the 384-dim embeddings using L2 distance for similarity search during the RAG process
        self.index = faiss.IndexFlatL2(384)
        
        # storing the raw text chunks which can be used later to fetch original context after similarity search
        self.metadata = []

    def load_and_split(self, docx_path):
        loader = Docx2txtLoader(docx_path)
        data = loader.load()
        chunks = self.text_splitter.split_documents(data)
        return chunks

    def embed_documents(self, chunks):
        texts = [chunk.page_content for chunk in chunks]
        embeddings = self.embedder.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))
        
        # Save metadata for reverse lookup
        self.metadata.extend(texts)  

    def save_index(self):
        with open(self.index_path, 'wb') as f:
            pickle.dump((self.index, self.metadata), f)

    def build_index_from_docs(self, doc_paths):
        for path in doc_paths:
            chunks = self.load_and_split(path)
            self.embed_documents(chunks)
        self.save_index()