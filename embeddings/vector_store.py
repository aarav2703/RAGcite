# embeddings/vector_store.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict

# Load sentence-transformer model
embedder = SentenceTransformer("all-MiniLM-L6-v2")


class VectorStore:
    def __init__(self):
        self.text_chunks: List[str] = []
        self.metadata: List[Dict] = []
        self.index = None
        self.dimension = embedder.get_sentence_embedding_dimension()

    def add_documents(self, documents: List[Dict]):
        """
        Adds and indexes documents.

        Each document must have:
            - 'text': The chunk to embed
            - 'meta': Metadata dictionary (e.g., title, link)
        """
        embeddings = embedder.encode(
            [doc["text"] for doc in documents], convert_to_numpy=True
        )

        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)

        self.index.add(embeddings)
        self.text_chunks.extend([doc["text"] for doc in documents])
        self.metadata.extend([doc["meta"] for doc in documents])

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Searches the index for top_k most similar results to the query.
        Returns list of dicts with matched text and metadata.
        """
        query_embedding = embedder.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.text_chunks):
                results.append(
                    {"text": self.text_chunks[idx], "meta": self.metadata[idx]}
                )

        return results
