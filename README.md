# PAU

**Author**: Anurag Atulya  
**PAU**: Personal Assistant for Upskilling  
**Purpose**: Develop a **scalable**, **extensible**, and **human-centric** framework for building personal upskilling assistants powered by **advanced AI** and **human psychology** principles.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Project Goals](#project-goals)  
3. [Directory Structure](#directory-structure)  
4. [Core Components](#core-components)  
5. [Setup Instructions](#setup-instructions)  
6. [Usage](#usage)  
7. [Future Development](#future-development)  
8. [Upcoming Next](#upcoming-next)

---

## 1. Introduction

**PAU** is an open-source framework designed to build personal **upskilling assistants**. It integrates AI features like **memory**, **intuitive reasoning**, **search**, and newly added **digital vision processing** (for OCR and screenshot capture). The framework is **modular**, **scalable**, and intended to support long-term growth, supporting both developers and end-users.

Recent enhancements include:

- **Landing Page** that greets users, stores their names in a JSON file, and navigates to either **Sync With PAU** or a **Playground**.  
- **Advanced Memory** system with vector storage (FAISS or Chroma) plus a knowledge graph for storing relationships.  
- **DigitalVision** pipeline for **screenshot capture**, with optional **OCR** and **local LLM** processing.  

---

## 2. Project Goals

1. **Open Framework**: Provide a reusable base for developers to create personal assistants.  
2. **Human-Centric AI**: Integrate psychology-driven algorithms for more natural interactions.  
3. **Scalability**: Support modular growth (e.g., social media integration, digital vision).  
4. **Transparency**: Log all activities for user monitoring and AI synchronization.  
5. **Extensibility**: Allow the addition of custom AI functions (e.g., memory, intuition, vision).  

---

## 3. Directory Structure

Below is a simplified overview. Adjust as your code grows:

```plaintext
PAU/
├── app.py                          # Main entry point for the backend
├── requirements.txt               # Python dependencies
├── database/                      # Database, migrations, knowledge
│   ├── knowledge/                 # Markdown documents for RAG search
│   ├── screen_snapshot/           # Screenshots captured by DigitalVision
│   └── processed_logs/            # OCR + LLM processed text files
├── pau/
│   ├── routes/                    # API routes
│   │   ├── chatbot_routes.py      # Chatbot & memory routes
│   │   ├── search_routes.py       # Search endpoints
│   │   └── ...
│   ├── services/                  # Core logic & services
│   │   ├── advanced_memory.py     # Advanced memory (Chroma/FAISS + graph)
│   │   ├── ai_engine.py           # LLM calls
│   │   ├── digital_vision.py      # Screenshot capture + optional OCR pipeline
│   │   └── ...
│   └── utils/                     # Utilities (logging, validation, etc.)
├── public/                        # Frontend static files
│   ├── index.html                 # Main UI
│   ├── graph_inspector.html       # Visualizes memory graph with Vis.js
│   └── ...
└── docs/                          # Project documentation
```

---

## 4. Core Components

### 1. **`app.py`**
- **Main** Flask application.  
- Registers routes, sets up the server.  
- Initializes advanced memory or any digital vision pipeline if needed.

### 2. **Routes (`pau/routes/`)**
- **Chatbot** (`chatbot_routes.py`):  
  - Manages chat logic, memory storage, retrieving advanced memory, plus endpoints for memory reward/penalty.  
  - Exposes `/api/chat` and `/api/memory/...`.
- **Search** (`search_routes.py`):  
  - Provides endpoints for RAG search or knowledge-based retrieval.

### 3. **Services (`pau/services/`)**
- **`advanced_memory.py`**:  
  - Combines vector DB (FAISS/Chroma) with a knowledge graph (NetworkX) to store relationships.  
  - Offers store/retrieve functions plus RL-based weighting.  
- **`ai_engine.py`**:  
  - Handles LLM calls (e.g., local llama model or remote endpoints).  
- **`digital_vision.py`**:  
  - Captures screenshots (with mss or custom approach).  
  - (Optional) Runs OCR + LLM-based parsing pipeline.  

### 4. **Database & Data Folders (`database/`)**
- **`knowledge/`**:  
  - Markdown docs used by RAG search.  
- **`screen_snapshot/`**:  
  - Where DigitalVision saves screenshots (e.g., `DigitalVision_monitor1_20250211_185544.png`).  
- **`processed_logs/`**:  
  - Where we store `.md` or `.json` files after OCR + LLM parse.

### 5. **Frontend (`public/`)**
- **`index.html`**:  
  - Main UI for chat and memory usage.  
  - Contains a “View Memory Graph” button linking to `/graph_inspector`.  
- **`graph_inspector.html`**:  
  - Uses Vis.js to fetch `/api/memory/graph` and render the entire memory graph visually.

---

## 5. Setup Instructions

### 1. **Prerequisites**
- Python 3.8+  
- Tesseract OCR (for optional OCR functionality)  
- Local LLM (like `llama-3.2-1b-instruct`) if you plan to parse text locally.  
- (Optional) Docker if you want container-based deployment.

### 2. **Installation**
```bash
git clone https://github.com/your-username/PAU.git
cd PAU
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. **Configuration**
- **Set** environment variables or `.env` for sensitive data if needed.  
- **Check** `digital_vision.py` or `advanced_memory.py` for any custom endpoints or file paths.

### 4. **Run the Application**
```bash
python app.py
```
Open `http://127.0.0.1:5000/` in your browser to see the main UI.

---

## 6. Usage

1. **Landing Page**  
   - **Greets** the user, storing the user’s name.  
   - Offers navigation to the main PAU or Playground.

2. **Chat Interface**  
   - **Type** messages in the left panel.  
   - PAU **retrieves** relevant memory (from advanced_memory).  
   - You see LLM-based responses on the right side.

3. **View Memory Graph**  
   - Click “View Memory Graph” in the main UI.  
   - Loads `graph_inspector.html`, fetches `/api/memory/graph`, and displays an interactive node-link diagram of all stored memories and relationships (persons, places, etc.).

4. **Digital Vision** (Optional)  
   - If configured, a **background** or manual pipeline captures screenshots in `data/screen_snapshot/`.  
   - You can run OCR + local LLM parse to store structured text in `data/processed_logs/`.

---

## 7. Future Development

1. **AI Enhancements**  
   - Improved context-aware reasoning, emotional simulation, long-term memory management.  
2. **Further Frontend Development**  
   - Migrate or expand UI with a modern frontend framework (React, Vue, etc.).  
3. **Social Media Integration**  
   - Potential for shared progress tracking or user collaboration.  
4. **Extended Logging & Monitoring**  
   - Real-time dashboards for performance metrics, error tracking, user insights.  
5. **Plugin Ecosystem**  
   - Third-party modules for specialized AI tasks or advanced knowledge retrieval.

---

## 8. Upcoming Next

Here are **four** major features planned for the near future:

1. **Digital Vision Processing**  
   - We’ll refine the existing screenshot pipeline to include **OCR** and possibly advanced **vision models** (object detection, classification).  
   - The pipeline will store recognized text (or objects) in an **advanced memory** store for easy retrieval.

2. **Searching Memory from Digital Vision**  
   - A new **search function** that specifically queries the memory derived from screenshots or images.  
   - For instance, you could type “Show me all screenshots that mentioned ‘deadline’ last week” and get relevant images plus extracted text.

3. **Skill Testing in Various Fields**  
   - Introduce an **interactive quiz** or test mode.  
   - The system can ask daily questions in different domains (coding, math, language), track your performance, and provide feedback or progress charts.

4. **LLM-Based Intuitive Evaluation**  
   - On a **daily** or scheduled basis, PAU will evaluate user skills using an **LLM** to gauge strengths/weaknesses.  
   - The system can automatically suggest areas to improve, generate specialized exercises, or highlight user’s best fields.

Stay tuned for these expansions, as they will make PAU a truly holistic personal upskilling assistant—combining **digital vision** capabilities, advanced memory, skill testing, and daily LLM-driven introspection.

---

**Let’s build PAU together and redefine personal upskilling!**