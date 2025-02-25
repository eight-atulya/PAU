#!/usr/bin/env python
"""
Memory with Branches, Filtered Search, and Closed-Loop Knowledge Generation

Features:
  1. Memory is divided into 8 branches: person, time, sentiments, work, personal, finance, health, others.
  2. When searching, you can filter by branch.
  3. A closed-loop system uses the local LLM to generate new knowledge from user queries.
  4. Uses local embedding model and LLM inference.

Before running:
  - Update EMBED_ENDPOINT, MODEL_NAME, and LLM settings below.
  - Ensure your local endpoints are running.
  - Install required packages:
      pip install requests openai rich networkx faiss-cpu torch spacy
      python -m spacy download en_core_web_sm
  - Create a "knowledge" folder with your .txt/.md documents.
"""

import os
import time
import pickle
import random
import hashlib
from collections import deque
import numpy as np
import networkx as nx
import torch
import torch.nn as nn
import torch.nn.functional as F
import faiss
import spacy
import requests
import openai

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

###############################################################################
# Global Settings & Branch Definitions
###############################################################################
BRANCHES = ["person", "time", "sentiments", "work", "personal", "finance", "health", "others"]

###############################################################################
# Inference Endpoints
###############################################################################
EMBED_ENDPOINT = "http://192.168.1.113:1234/v1/embeddings"
MODEL_NAME = "text-embedding-nomic-embed-text-v1.5"

def get_embedding(text: str) -> list:
    payload = {"model": MODEL_NAME, "input": text}
    headers = {"Content-Type": "application/json"}
    resp = requests.post(EMBED_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    embedding = data["data"][0]["embedding"]
    return embedding

# LLM Inference (local LLM via LM Studio API)
openai.api_key = "lm-studio"  # Update if needed
openai.api_base = "http://localhost:1234/v1"

def generate_response(prompt, model="model-identifier"):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return completion.choices[0].message.content

###############################################################################
# 0) Utility: SpaCy for Text Chunking
###############################################################################
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None
    print("[WARNING] spaCy model not found. Run: python -m spacy download en_core_web_sm")

###############################################################################
# 1) Connectome (Semantic Network)
###############################################################################
class Connectome:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_concept(self, concept_id, **attrs):
        self.graph.add_node(concept_id, **attrs)

    def add_relationship(self, source, target, relation="related_to", weight=1.0, **attrs):
        self.graph.add_edge(source, target, relation=relation, weight=weight, **attrs)

    def neighbors_of(self, node_id):
        return list(self.graph[node_id].keys()) if node_id in self.graph else []

    def update_edge_weight(self, source, target, delta=0.1):
        if self.graph.has_edge(source, target):
            w = self.graph[source][target].get("weight", 1.0)
            self.graph[source][target]["weight"] = w + delta

    def multi_hop_search(self, start_node, max_depth=2):
        visited = set()
        frontier = deque([(start_node, 0)])
        results = []
        while frontier:
            current, depth = frontier.popleft()
            if current not in visited:
                visited.add(current)
                results.append((current, depth))
                if depth < max_depth:
                    for neighbor in self.neighbors_of(current):
                        frontier.append((neighbor, depth + 1))
        return results

###############################################################################
# 2) Hippocampus (Key-Value Store for Chunks)
###############################################################################
class Hippocampus:
    def __init__(self):
        self.memory_store = {}

    def add_memory(self, chunk_id, data):
        self.memory_store[chunk_id] = data

    def get_memory(self, chunk_id):
        return self.memory_store.get(chunk_id)

    def update_feedback(self, chunk_id, feedback_delta):
        mem = self.memory_store.get(chunk_id)
        if mem:
            mem["feedback"] = mem.get("feedback", 0.0) + feedback_delta

    def update_reward(self, chunk_id, reward_delta):
        mem = self.memory_store.get(chunk_id)
        if mem:
            mem["RL_reward"] = mem.get("RL_reward", 0.0) + reward_delta

###############################################################################
# 3) Neocortex (FAISS HNSW Index for Similarity Search)
###############################################################################
class Neocortex:
    def __init__(self, embedding_dim, m=32):
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexHNSWFlat(embedding_dim, m, faiss.METRIC_L2)
        self.index.hnsw.efConstruction = 200
        self.index.hnsw.efSearch = 64
        self.embeddings = []
        self.keys = []

    def add_vectors(self, vectors, keys):
        vectors = np.array(vectors, dtype=np.float32)
        self.index.add(vectors)
        self.embeddings.extend(vectors)
        self.keys.extend(keys)

    def search(self, query_vec, top_k=5, creative=False):
        if len(query_vec.shape) == 1:
            query_vec = query_vec[None, :]
        k = top_k * 3 if creative else top_k
        distances, indices = self.index.search(query_vec, k)
        results = [(self.keys[idx], distances[0][rank]) for rank, idx in enumerate(indices[0])]
        if creative:
            direct = results[:top_k]
            remainder = results[top_k:]
            random.shuffle(remainder)
            final = direct + (remainder[:2] if len(remainder) >= 2 else remainder)
            final.sort(key=lambda x: x[1])
            return final
        return results[:top_k]

    def robust_search(self, query_vec, top_k=5):
        if self.index.ntotal == 0:
            return []
        if len(query_vec.shape) == 1:
            query_vec = query_vec[None, :]
        distances, indices = self.index.search(query_vec, top_k)
        results = [(self.keys[idx], distances[0][rank]) for rank, idx in enumerate(indices[0])]
        return results if results else [("NO_RESULT", 9999.0)]

    def rebuild_index(self):
        self.index = faiss.IndexHNSWFlat(self.embedding_dim, 32, faiss.METRIC_L2)
        self.index.hnsw.efConstruction = 200
        self.index.hnsw.efSearch = 64
        if self.embeddings:
            self.index.add(np.array(self.embeddings, dtype=np.float32))

###############################################################################
# 4) PrefrontalCortex (Upgraded NTM for Short-Term Memory)
###############################################################################
class PrefrontalCortex(nn.Module):
    def __init__(self, input_dim, hidden_dim, mem_slots, mem_dim, output_dim):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.mem_slots = mem_slots
        self.mem_dim = mem_dim
        self.controller = nn.LSTMCell(input_dim + mem_dim, hidden_dim)
        self.read_fc = nn.Linear(self.hidden_dim, self.mem_dim)
        self.head_fc = nn.Linear(hidden_dim, mem_dim*3 + mem_slots + 1)
        self.output_fc = nn.Linear(hidden_dim + mem_dim, output_dim)
        self.register_buffer("memory", torch.zeros(mem_slots, mem_dim))
        self.register_buffer("usage", torch.zeros(mem_slots))

    def reset_memory(self):
        self.memory.zero_()
        self.usage.zero_()

    def forward(self, x, prev_state=None):
        if prev_state is None:
            h_prev = torch.zeros(1, self.hidden_dim, device=x.device)
            c_prev = torch.zeros(1, self.hidden_dim, device=x.device)
        else:
            h_prev, c_prev = prev_state

        # Read from memory
        read_key = torch.tanh(self.read_fc(h_prev))
        sim = torch.mv(self.memory, read_key[0])
        read_weights = F.softmax(sim, dim=0)
        read_vector = torch.mv(self.memory.t(), read_weights).unsqueeze(0)
        for i in range(self.mem_slots):
            self.usage[i] += read_weights[i].item()

        # Update controller
        input_combined = torch.cat([x, read_vector], dim=1)
        h_new, c_new = self.controller(input_combined, (h_prev, c_prev))

        # Generate write parameters and update memory
        params = self.head_fc(h_new)[0]
        write_key = torch.tanh(params[:self.mem_dim])
        erase_vec = torch.sigmoid(params[self.mem_dim:2*self.mem_dim])
        add_vec   = torch.tanh(params[2*self.mem_dim:3*self.mem_dim])
        w_logits  = params[3*self.mem_dim:3*self.mem_dim + self.mem_slots]
        write_gate= torch.sigmoid(params[-1])
        w_weights = F.softmax(w_logits, dim=0)

        new_mem = []
        for i in range(self.mem_slots):
            w_i = w_weights[i] * write_gate
            m_i = self.memory[i]
            if self.usage[i] < 0.1:
                m_i = torch.zeros_like(m_i)
            m_i_erased = m_i * (1.0 - w_i * erase_vec)
            m_i_new = m_i_erased + w_i * add_vec
            new_mem.append(m_i_new.unsqueeze(0))
        updated_memory = torch.cat(new_mem, dim=0)
        self.memory.copy_(updated_memory)
        out = self.output_fc(torch.cat([h_new, read_vector], dim=1))
        return out, (h_new, c_new)

    def train_on_sequence(self, seq_inputs, seq_targets, epochs=200, lr=1e-3):
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        loss_fn = nn.MSELoss()
        for epoch in range(epochs):
            self.reset_memory()
            h, c = None, None
            epoch_loss = 0.0
            for inp, tgt in zip(seq_inputs, seq_targets):
                out, (h, c) = self.forward(inp, (h, c))
                loss = loss_fn(out, tgt)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item()
            if (epoch+1) % 50 == 0:
                print(f"[NTM-Train] Epoch={epoch+1}, Loss={epoch_loss/len(seq_inputs):.4f}")

###############################################################################
# 5) HumanBrain (Master Class with Branches, Caching, and Closed-Loop Generation)
###############################################################################
class HumanBrain:
    def __init__(self, embed_dim=768, cache_path="data/doc_cache.pkl"):
        self.connectome = Connectome()
        self.hippocampus = Hippocampus()
        self.neocortex = Neocortex(embedding_dim=embed_dim)
        self.prefrontal_cortex = PrefrontalCortex(input_dim=embed_dim, hidden_dim=64,
                                                  mem_slots=16, mem_dim=32, output_dim=32)
        self.embed_dim = embed_dim
        self.cache_path = cache_path
        self.doc_cache = self.load_doc_cache()

    def load_doc_cache(self):
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "rb") as f:
                    cache = pickle.load(f)
                print("[HumanBrain] Document cache loaded.")
                return cache
            except Exception as e:
                print(f"[WARNING] Failed to load document cache: {e}")
        return {}

    def save_doc_cache(self):
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(self.doc_cache, f)
            print("[HumanBrain] Document cache saved.")
        except Exception as e:
            print(f"[WARNING] Failed to save document cache: {e}")

    def compute_file_hash(self, file_path):
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()

    def embed_text(self, text):
        try:
            emb = get_embedding(text)
            return np.array(emb, dtype=np.float32)
        except Exception as e:
            print(f"[WARNING] Embedding inference failed: {e}")
            return np.random.rand(self.embed_dim).astype(np.float32)

    def chunk_text(self, text):
        chunks = []
        if not nlp:
            chunk_size = 300
            overlap = 50
            idx = 0
            while idx < len(text):
                chunks.append((text[idx: idx+chunk_size], ""))
                idx += (chunk_size - overlap)
            return chunks
        doc = nlp(text)
        for sent in doc.sents:
            parse_summary = " | ".join(f"{token.text}-{token.dep_}->{token.head.text}" for token in sent)
            entities = [ent.text for ent in sent.ents]
            enriched_parse = f"{parse_summary} | Entities: {', '.join(entities)}" if entities else parse_summary
            chunks.append((sent.text.strip(), enriched_parse))
        return chunks

    def classify_text_branch(self, text):
        # Use the LLM to classify text into one of the predefined branches.
        prompt = (f"Classify the following text into one of these branches: {', '.join(BRANCHES)}.\n"
                  f"Return only one branch (exactly one word):\n\n{text}\n\nAnswer:")
        branch = generate_response(prompt, model="model-identifier").strip().lower()
        if branch not in BRANCHES:
            branch = "others"
        return branch

    def ingest_document(self, text, doc_id=None, domain="general", doc_link=None, branch=None):
        if doc_id is None:
            doc_id = f"doc_{int(time.time())}"
        # If branch not provided, classify the text using LLM.
        if branch is None:
            branch = self.classify_text_branch(text)
        # Add branch info to the document node.
        self.connectome.add_concept(doc_id, type="document", domain=domain, doc_link=doc_link, branch=branch)
        sents_with_parse = self.chunk_text(text)
        batch_vecs, batch_keys = [], []
        for i, (sent_str, parse_str) in enumerate(sents_with_parse):
            vec = self.embed_text(sent_str)
            chunk_id = f"{doc_id}_chunk_{i}"
            metadata = {
                "text": sent_str,
                "domain": domain,
                "parse_tree": parse_str,
                "timestamp": time.time(),
                "feedback": 0.0,
                "RL_reward": 0.0,
                "doc_link": doc_link,
                "branch": branch
            }
            self.hippocampus.add_memory(chunk_id, metadata)
            self.connectome.add_concept(chunk_id, type="chunk", parse_tree=parse_str, doc_link=doc_link, branch=branch)
            self.connectome.add_relationship(doc_id, chunk_id, relation="has_chunk")
            batch_vecs.append(vec)
            batch_keys.append(chunk_id)
        if batch_vecs:
            self.neocortex.add_vectors(np.array(batch_vecs, dtype=np.float32), batch_keys)
        print(f"[HumanBrain] Ingested doc {doc_id} ({branch}) with {len(sents_with_parse)} chunks.")
        return {
            "doc_id": doc_id,
            "chunks": sents_with_parse,
            "embeddings": batch_vecs,
            "domain": domain,
            "timestamp": time.time(),
            "doc_link": doc_link,
            "branch": branch
        }

    def ingest_document_from_file(self, file_path, doc_id=None, domain="general"):
        file_hash = self.compute_file_hash(file_path)
        if doc_id is None:
            doc_id = os.path.splitext(os.path.basename(file_path))[0]
        doc_link = os.path.abspath(file_path)
        cached_entry = self.doc_cache.get(doc_id)
        if cached_entry and cached_entry.get("file_hash") == file_hash:
            print(f"[HumanBrain] Using cached data for {doc_id}.")
            sents_with_parse = cached_entry["chunks"]
            batch_vecs = cached_entry["embeddings"]
            branch = cached_entry.get("branch", "others")
            self.connectome.add_concept(doc_id, type="document", domain=domain, doc_link=doc_link, branch=branch)
            for i, (sent_str, parse_str) in enumerate(sents_with_parse):
                chunk_id = f"{doc_id}_chunk_{i}"
                metadata = {
                    "text": sent_str,
                    "domain": domain,
                    "parse_tree": parse_str,
                    "timestamp": cached_entry["timestamp"],
                    "feedback": 0.0,
                    "RL_reward": 0.0,
                    "doc_link": doc_link,
                    "branch": branch
                }
                self.hippocampus.add_memory(chunk_id, metadata)
                self.connectome.add_concept(chunk_id, type="chunk", parse_tree=parse_str, doc_link=doc_link, branch=branch)
                self.connectome.add_relationship(doc_id, chunk_id, relation="has_chunk")
            if batch_vecs:
                arr = np.array(batch_vecs, dtype=np.float32)
                keys = [f"{doc_id}_chunk_{i}" for i in range(len(sents_with_parse))]
                self.neocortex.add_vectors(arr, keys)
        else:
            print(f"[HumanBrain] Processing file {doc_id} (new or changed).")
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            processed_data = self.ingest_document(text, doc_id=doc_id, domain=domain, doc_link=doc_link)
            processed_data["file_hash"] = file_hash
            self.doc_cache[doc_id] = processed_data
            self.save_doc_cache()

    def query(self, query_text, top_k=5, creative=False, branch_filter=None):
        q_vec = self.embed_text(query_text)
        results = self.neocortex.search(q_vec, top_k=top_k, creative=creative)
        final = []
        for chunk_id, dist in results:
            mem = self.hippocampus.get_memory(chunk_id)
            # If branch_filter is specified, only include if branch matches.
            if branch_filter:
                if mem.get("branch", "others") not in branch_filter:
                    continue
            final.append({"chunk_id": chunk_id, "distance": dist, "metadata": mem})
        return final

    def robust_query(self, query_text, top_k=5, branch_filter=None):
        q_vec = self.embed_text(query_text)
        results = self.neocortex.robust_search(q_vec, top_k=top_k)
        final = []
        for chunk_id, dist in results:
            mem = self.hippocampus.get_memory(chunk_id)
            if branch_filter:
                if mem.get("branch", "others") not in branch_filter:
                    continue
            final.append({"chunk_id": chunk_id, "distance": dist, "metadata": mem})
        return final

    def short_term_think(self, input_text):
        vec = self.embed_text(input_text)
        x_torch = torch.from_numpy(vec).unsqueeze(0)
        out, _ = self.prefrontal_cortex(x_torch)
        return out.detach().cpu().numpy()

    def user_feedback(self, chunk_id, feedback_delta=1.0):
        self.hippocampus.update_feedback(chunk_id, feedback_delta)
        doc_id = chunk_id.split("_chunk_")[0]
        if self.connectome.graph.has_edge(doc_id, chunk_id):
            self.connectome.update_edge_weight(doc_id, chunk_id, delta=feedback_delta/10.0)

    def apply_rl_reward(self, chunk_id, reward_delta=0.5):
        self.hippocampus.update_reward(chunk_id, reward_delta)
        doc_id = chunk_id.split("_chunk_")[0]
        if self.connectome.graph.has_edge(doc_id, chunk_id):
            self.connectome.update_edge_weight(doc_id, chunk_id, delta=reward_delta/10.0)

    def multi_hop_retrieve(self, start_node, max_depth=2):
        return self.connectome.multi_hop_search(start_node, max_depth=max_depth)

    def rebuild_neocortex(self):
        self.neocortex.rebuild_index()

    def save_brain(self, path="data/human_brain.pkl"):
        index_path = os.path.join(os.path.dirname(path), "neocortex.index")
        index_clone = faiss.clone_index(self.neocortex.index)
        faiss.write_index(index_clone, index_path)
        data = {
            "hippocampus": self.hippocampus.memory_store,
            "graph": nx.to_dict_of_dicts(self.connectome.graph),
            "pfc_state": self.prefrontal_cortex.state_dict(),
            "embeddings": np.array(self.neocortex.embeddings, dtype=np.float32),
            "keys": self.neocortex.keys,
            "embed_dim": self.embed_dim,
            "doc_cache": self.doc_cache
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(data, f)
        self.save_doc_cache()
        print("[HumanBrain] Brain saved.")

    def load_brain(self, path="data/human_brain.pkl"):
        with open(path, "rb") as f:
            data = pickle.load(f)
        self.hippocampus.memory_store = data["hippocampus"]
        self.connectome.graph = nx.from_dict_of_dicts(data["graph"], create_using=nx.DiGraph)
        self.prefrontal_cortex.load_state_dict(data["pfc_state"])
        self.neocortex.embeddings = data["embeddings"].tolist()
        self.neocortex.keys = data["keys"]
        self.neocortex.embedding_dim = data["embed_dim"]
        self.embed_dim = data["embed_dim"]
        self.doc_cache = data.get("doc_cache", {})
        index_path = os.path.join(os.path.dirname(path), "neocortex.index")
        if os.path.exists(index_path):
            self.neocortex.index = faiss.read_index(index_path)
        else:
            print("[WARNING] No Neocortex index found, starting empty.")
        print("[HumanBrain] Brain loaded.")

    def clear_doc_cache(self):
        self.doc_cache = {}
        self.save_doc_cache()
        print("[HumanBrain] Document cache cleared.")

    def closed_loop_generate_knowledge(self, query):
        """
        Uses the LLM to generate new knowledge based on the query.
        The generated text is then ingested as a new document.
        """
        prompt = f"Based on the following query: '{query}', generate new knowledge or insights that could improve search and understanding."
        new_knowledge = generate_response(prompt, model="model-identifier")
        # Classify new knowledge into a branch
        branch = self.classify_text_branch(new_knowledge)
        doc_id = f"closed_loop_{int(time.time())}"
        self.ingest_document(new_knowledge, doc_id=doc_id, domain="closed_loop", doc_link=None, branch=branch)
        print(f"[HumanBrain] Closed-loop knowledge generated and ingested under branch '{branch}'.")
        return new_knowledge

###############################################################################
# 6) Interactive CLI with Branch Filter and Closed-Loop Option
###############################################################################
def display_results(results, console):
    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return
    table = Table(title="Recall Results")
    table.add_column("Chunk ID", style="cyan", no_wrap=True)
    table.add_column("Distance", style="magenta")
    table.add_column("Text", style="white")
    table.add_column("Branch", style="green")
    table.add_column("Doc Link", style="blue")
    for res in results:
        metadata = res.get("metadata", {})
        text = metadata.get("text", "N/A")
        chunk_id = res.get("chunk_id", "N/A")
        distance = f"{res.get('distance', 'N/A'):.4f}" if isinstance(res.get('distance'), float) else str(res.get('distance'))
        branch = metadata.get("branch", "N/A")
        doc_link = metadata.get("doc_link", "N/A")
        doc_link_rendered = f"[link={doc_link}]{doc_link}[/link]" if doc_link != "N/A" else "N/A"
        table.add_row(chunk_id, distance, text, branch, doc_link_rendered)
    console.print(table)

def interactive_mode(brain, console):
    console.print(Panel.fit("[bold blue]Interactive Recall CLI[/bold blue]\nType your query below (or 'exit' to quit):"))
    while True:
        query = input("\n[Query] > ").strip()
        if query.lower() in ["exit", "quit"]:
            break
        # Ask for optional branch filtering (comma-separated)
        branch_filter_input = input("Enter branch filters (comma-separated) or press enter to skip: ").strip().lower()
        branch_filter = [b.strip() for b in branch_filter_input.split(",") if b.strip()] if branch_filter_input else None
        creative = input("Use creative mode? (y/n): ").strip().lower() == "y"
        robust = input("Use robust mode? (y/n): ").strip().lower() == "y"
        if robust:
            results = brain.robust_query(query, top_k=5, branch_filter=branch_filter)
        else:
            results = brain.query(query, top_k=5, creative=creative, branch_filter=branch_filter)
        display_results(results, console)
        # Option to generate closed-loop knowledge
        if input("Generate new knowledge based on query? (y/n): ").strip().lower() == "y":
            new_knowledge = brain.closed_loop_generate_knowledge(query)
            console.print(f"\n[bold green]New Knowledge Generated:[/bold green]\n{new_knowledge}")
        # Option to get LLM additional insights
        if input("Generate additional LLM response for query? (y/n): ").strip().lower() == "y":
            prompt = f"Based on the query: '{query}', provide additional insights."
            llm_response = generate_response(prompt)
            console.print(f"\n[bold green]LLM Response:[/bold green]\n{llm_response}")

###############################################################################
# Main: Run Interactive CLI
###############################################################################
if __name__ == "__main__":
    console = Console()
    brain = HumanBrain(embed_dim=768)
    brain_file = "data/human_brain.pkl"
    if os.path.exists(brain_file):
        brain.load_brain(brain_file)
        console.print(f"[bold green]Brain loaded from {brain_file}[/bold green]")
    else:
        console.print(f"[bold red]No brain file found at {brain_file}. Starting with an empty brain.[/bold red]")

    # Ingest documents from the 'knowledge' folder
    knowledge_dir = "./knowledge"
    if os.path.exists(knowledge_dir):
        for fname in os.listdir(knowledge_dir):
            if fname.endswith(".txt") or fname.endswith(".md"):
                fpath = os.path.join(knowledge_dir, fname)
                brain.ingest_document_from_file(fpath, doc_id=fname.replace(".", "_"), domain="knowledge")
    else:
        console.print("[INFO] No 'knowledge' folder found; skipping document ingestion.")

    # Run interactive CLI
    interactive_mode(brain, console)
    # Save brain state on exit
    brain.save_brain("data/human_brain.pkl")
