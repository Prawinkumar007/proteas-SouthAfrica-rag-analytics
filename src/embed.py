import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import json
import os
import numpy as np

def generate_embeddings(input_file, output_index, output_metadata):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run ingest.py first.")
        return

    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} events. Generating embeddings...")

    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Process in batches
    texts = df['text'].tolist()
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Save index
    faiss.write_index(index, output_index)

    # Save metadata
    metadata = df.to_dict(orient='records')
    with open(output_metadata, 'w') as f:
        json.dump(metadata, f)

    print(f"--- Embedding Summary ---")
    print(f"Total embeddings generated: {len(embeddings)}")
    print(f"Index size: {os.path.getsize(output_index) / 1024:.2f} KB")
    print(f"Saved index to {output_index} and metadata to {output_metadata}")

if __name__ == "__main__":
    os.makedirs("embeddings", exist_ok=True)
    generate_embeddings(
        "data/processed_events.csv", 
        "embeddings/cricket_index.faiss", 
        "embeddings/metadata.json"
    )
