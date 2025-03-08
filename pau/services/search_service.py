import requests
import os
import faiss
import numpy as np

def chunk_text(text: str, chunk_size=500, overlap=50):
    """
    Splits `text` into overlapping chunks of `chunk_size` length.
    Overlap is optional (e.g., 50 chars repeated to maintain context).
    Returns a list of chunk strings.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

EMBED_ENDPOINT = "http://192.168.31.228:1234/v1/embeddings"
MODEL_NAME = "text-embedding-nomic-embed-text-v1.5"

def get_embedding(text: str) -> list:
    payload = {
        "model": MODEL_NAME,
        "input": text
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(EMBED_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    
    # Assuming the API returns something like {"data":[{"embedding": [...]}]}
    embedding = data["data"][0]["embedding"]
    return embedding


INDEX_PATH = "database/faiss_index.bin"  # Or wherever you like

def build_faiss_index(knowledge_folder="database/knowledge"):
    # Ensure the directory exists
    os.makedirs(knowledge_folder, exist_ok=True)    
    
    # Create a default file if the directory is empty
    if not os.listdir(knowledge_folder):
        default_file_path = os.path.join(knowledge_folder, "seed_knowledge.md")
        with open(default_file_path, "w", encoding="utf-8") as f:
            f.write("How humanity needs to become more efficient.")
    
    # copies the screen_history knowledge to the knowledge folder
    screen_history_folder = "brain/knowledge/screen_history"
    for filename in os.listdir(screen_history_folder):
        if filename.endswith(".md"):
            src_path = os.path.join(screen_history_folder, filename)
            dest_path = os.path.join(knowledge_folder, filename)
            with open(src_path, "r", encoding="utf-8") as src_file:
                with open(dest_path, "w", encoding="utf-8") as dest_file:
                    dest_file.write(src_file.read())

    
    all_embeddings = []
    metadata = []
    for filename in os.listdir(knowledge_folder):
        if filename.endswith(".md"):
            filepath = os.path.join(knowledge_folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            # chunk the doc
            chunks = chunk_text(text, chunk_size=500, overlap=50)
            
            for i, chunk in enumerate(chunks):
                # embed chunk
                emb = get_embedding(chunk)
                all_embeddings.append(emb)
                metadata.append({
                    "document": filename,
                    "chunk": chunk,
                    "chunk_index": i
                })

    # Convert to np.array
    embeddings_np = np.array(all_embeddings, dtype=np.float32)
    # dimension (embedding_dim) from the first vector
    embedding_dim = embeddings_np.shape[1]

    # Build the FAISS index
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings_np)

    # Save index and metadata
    faiss.write_index(index, INDEX_PATH)

    # Also store metadata in a separate file
    import pickle
    with open("database/faiss_metadata.pkl", "wb") as m:
        pickle.dump(metadata, m)

    print("FAISS index built and saved.")


def load_faiss_resources():
    # Load index
    index = faiss.read_index(INDEX_PATH)
    # Load metadata
    import pickle
    with open("database/faiss_metadata.pkl", "rb") as m:
        metadata = pickle.load(m)
    return index, metadata

def search_faiss(query: str, k=3):
    # 1) embed query
    query_emb = get_embedding(query)
    query_np = np.array([query_emb], dtype=np.float32)

    # 2) load index and metadata
    index, metadata = load_faiss_resources()

    # 3) do the search
    distances, indices = index.search(query_np, k)  # shape (1, k)
    
    # 4) gather results
    results = []
    for rank, idx in enumerate(indices[0]):
        chunk_data = metadata[idx]
        dist = distances[0][rank]
        result = {
            "document": chunk_data["document"],
            "chunk_text": chunk_data["chunk"],
            "chunk_index": chunk_data["chunk_index"],
            "distance": float(dist),
        }
        results.append(result)
    return results

