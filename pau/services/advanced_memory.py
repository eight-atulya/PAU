# pau/services/advanced_memory.py

import os
import time
import uuid

import requests
import numpy as np
import networkx as nx
import chromadb
from chromadb.config import Settings

########################
# 1) CUSTOM EMBEDDING
########################
EMBED_ENDPOINT = "http://192.168.1.113:1234/v1/embeddings"
MODEL_NAME = "text-embedding-nomic-embed-text-v1.5"

def get_embedding(text: str) -> list:
    payload = {"model": MODEL_NAME, "input": text}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(EMBED_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"][0]["embedding"]

########################
# 2) CHROMA CLIENT
########################
# Ensure the folder exists
os.makedirs("database/chroma_advanced", exist_ok=True)

CHROMA_SETTINGS = Settings(
    chroma_db_impl="duckdb+parquet",              # <--- Legacy approach
    persist_directory="database/chroma_advanced", # folder to store data
    anonymized_telemetry=False
)
chroma_client = chromadb.Client(CHROMA_SETTINGS)
memory_collection = chroma_client.get_or_create_collection(
    name="advanced_memory",
    metadata={"description": "Advanced memory with RL weighting and time decay"}
)

########################
# 3) NETWORKX GRAPH
########################
memory_graph = nx.DiGraph()

########################
# 4) LOCAL INDEX
########################
MEMORY_INDEX = {}  # doc_id => { 'importance': ..., 'rl_reward': ... }

########################
# 5) INIT & PERSIST
########################
def init_advanced_memory():
    """
    Optionally load a saved graph or other data.
    Called at application startup (e.g. in app.py).
    """
    load_graph()
    print("[init_advanced_memory] Initialized memory service.")

def persist_advanced_memory():
    """
    Explicitly persist Chroma data to disk.
    This ensures your advanced_memory is saved in 'database/chroma_advanced/'
    """
    chroma_client.persist()
    print("[persist_advanced_memory] Chroma data persisted to disk.")

def save_graph():
    """Optional: Save the NetworkX graph to a file."""
    path = "database/memory_graph.gpickle"
    nx.write_gpickle(memory_graph, path)
    print("[save_graph] memory_graph saved to", path)

def load_graph():
    """Optional: Load an existing graph from file if it exists."""
    path = "database/memory_graph.gpickle"
    if os.path.exists(path):
        global memory_graph
        memory_graph = nx.read_gpickle(path)
        print("[load_graph] memory_graph loaded from", path)

########################
# 6) CORE FUNCTIONS
########################
def store_advanced_memory(content: str, person: str = "", place: str = "", time_label: str = "", importance=1.0):
    """
    Store a memory with relationships in the graph + vector embeddings in Chroma.
    """
    doc_id = str(uuid.uuid4())
    now_ts = time.time()
    metadata = {
        "person": person,
        "place": place,
        "time_label": time_label,
        "importance": importance,
        "timestamp": now_ts
    }

    # 1) embed text
    emb = get_embedding(content)

    # 2) add to Chroma
    memory_collection.add(
        documents=[content],
        embeddings=[emb],
        metadatas=[metadata],
        ids=[doc_id]
    )

    # 3) local RL index
    MEMORY_INDEX[doc_id] = {
        "importance": importance,
        "rl_reward": 0.0
    }

    # 4) add relationships in the graph
    memory_graph.add_node(doc_id, content=content, **metadata)
    if person:
        memory_graph.add_node(person, label="person")
        memory_graph.add_edge(doc_id, person)
        memory_graph.add_edge(person, doc_id)
    if place:
        memory_graph.add_node(place, label="place")
        memory_graph.add_edge(doc_id, place)
        memory_graph.add_edge(place, doc_id)
    if time_label:
        memory_graph.add_node(time_label, label="time")
        memory_graph.add_edge(doc_id, time_label)
        memory_graph.add_edge(time_label, doc_id)

def retrieve_advanced_memories(query: str, top_k=5):
    """
    Retrieve relevant memories from Chroma + Weighted Decay + RL weighting.
    """
    query_emb = get_embedding(query)
    results = memory_collection.query(
        query_embeddings=[query_emb],
        n_results=top_k * 3
    )

    scored = []
    if results.get("ids"):
        for i, doc_id in enumerate(results["ids"][0]):
            doc_content = results["documents"][0][i]
            doc_meta = results["metadatas"][0][i]
            age = time.time() - doc_meta["timestamp"]
            # 30-day half-life
            decay_factor = pow(2, -(age / (60*60*24*30)))
            rl_reward = MEMORY_INDEX.get(doc_id, {}).get("rl_reward", 0.0)
            base_importance = doc_meta.get("importance", 1.0)
            sim_approx = 1.0 - (i * 0.05)
            final_score = sim_approx * base_importance * decay_factor + rl_reward
            scored.append((doc_id, final_score, doc_content, doc_meta))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_k_mem = scored[:top_k]

    memories = []
    for doc_id, score, content, meta in top_k_mem:
        memories.append({
            "doc_id": doc_id,
            "score": score,
            "content": content,
            "metadata": meta
        })
    return memories

def reward_memory(doc_id: str, reward_value: float = 1.0):
    if doc_id in MEMORY_INDEX:
        MEMORY_INDEX[doc_id]["rl_reward"] += reward_value

def reduce_memory_importance(doc_id: str, penalty=0.1):
    if doc_id in MEMORY_INDEX:
        MEMORY_INDEX[doc_id]["rl_reward"] -= penalty

def find_related_nodes(entity: str):
    """Return neighbors of an entity in memory_graph."""
    if entity not in memory_graph:
        return []
    return list(memory_graph[entity].keys())
