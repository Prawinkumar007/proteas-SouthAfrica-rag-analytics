import faiss
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

class CricketRetriever:
    def __init__(self, index_path="embeddings/cricket_index.faiss", metadata_path="embeddings/metadata.json"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.index = faiss.read_index(index_path)
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = None
            self.metadata = None
            print("Warning: Index or metadata not found. Please run embed.py.")

    def retrieve(self, query, top_k=5, filters=None):
        if self.index is None:
            return []

        # Convert query to embedding
        query_vector = self.model.encode([query]).astype('float32')
        
        # Search FAISS
        # If filters are provided, we might need a larger initial set and then filter manually
        # OR use FAISS IDMap but let's keep it simple with manual filtering for now
        
        search_k = top_k * 5 if filters else top_k
        distances, indices = self.index.search(query_vector, search_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx == -1: continue
            
            meta = self.metadata[idx]
            match = True
            
            if filters:
                for key, value in filters.items():
                    if key in meta and value != "All" and meta[key] != value:
                        match = False
                        break
            
            if match:
                results.append({
                    "text": meta['text'],
                    "score": float(distances[0][i]),
                    "metadata": meta
                })
            
            if len(results) >= top_k:
                break
                
        return results

    def get_similar_situations(self, match_context, top_k=3):
        return self.retrieve(match_context, top_k=top_k)

if __name__ == "__main__":
    # Test
    retriever = CricketRetriever()
    if retriever.index:
        res = retriever.retrieve("death overs bowling vs India")
        for r in res:
            print(f"Score: {r['score']:.4f} | {r['text']}")
