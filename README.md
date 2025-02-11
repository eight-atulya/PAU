# PAU

**Author**: Anurag Atulya  
**PAU**: Personal Assistant for Upskilling  
**Purpose**: Develop a scalable, extensible, and human-centric framework for building personal upskilling assistants powered by advanced AI and human psychology principles.

---

## Table of Contents

1. [Introduction](#introduction)  
2. [Project Goals](#project-goals)  
3. [Directory Structure](#directory-structure)  
4. [Core Components](#core-components)  
5. [Setup Instructions](#setup-instructions)  
6. [Usage](#usage)  
7. [New Features](#new-features)  
8. [Future Development](#future-development)

---

## Introduction

**PAU** is an open-source framework designed to build personal upskilling assistants. It integrates advanced AI functions—such as memory, intuition, and emotion simulation—with human-centric design principles, extensive logging, and data-driven user insights. The framework is modular, scalable, and designed for long-term growth, supporting both developers and end-users.

Recent enhancements include:
- A new **Landing Page** that greets users, stores their names in a JSON file, and provides navigation to the main interface or an experimental Playground.
- A **RAG search system** powered by a locally running embedding model and FAISS. This system chunks and embeds markdown documents stored in the knowledge folder and returns the most relevant chunks along with links to view the original files.
- An optional **watchdog** service that automatically monitors the knowledge folder for changes and updates the FAISS index accordingly.

---

## Project Goals

1. **Open Framework**: Provide a reusable base for developers to create personal assistants.  
2. **Human-Centric AI**: Integrate psychology-driven algorithms for natural and realistic interactions.  
3. **Scalability**: Support modular growth with features like social media integration and automated document ingestion.  
4. **Transparency**: Log all activities to enable user monitoring and effective AI synchronization.  
5. **Extensibility**: Allow the addition of custom AI functions (e.g., memory, intuition) and third-party integrations.

---

## Directory Structure

```plaintext
PAU/
├── README.md                      # Comprehensive project documentation (this file)
├── LICENSE                        # License for open-source use
├── CONTRIBUTING.md                # Guidelines for contributing to the project
├── app.py                         # Main entry point for the backend application
├── requirements.txt               # Python dependencies (includes faiss-cpu and watchdog)
├── .env                           # Environment variables for sensitive configs
├── pau/                           # Main backend application package
│   ├── __init__.py                # Initialize the application package
│   ├── config.py                  # Configuration settings for the app
│   ├── routes/                    # API routes (modular and extendable)
│   │   ├── __init__.py            # Register API blueprints
│   │   ├── chatbot_routes.py      # Chatbot-related API endpoints
│   │   ├── search_routes.py       # Search-related API endpoints (includes RAG search)
│   │   ├── notes_routes.py        # Notes-related API endpoints
│   │   ├── progress_routes.py     # Progress tracking endpoints
│   │   └── misc_routes.py         # Miscellaneous routes (e.g., serving markdown files)
│   ├── services/                  # Core business logic and services
│   │   ├── __init__.py            # Initialize services package
│   │   ├── ai_engine.py           # AI functions (e.g., memory, intuition, emotion)
│   │   ├── search_service.py      # Search-related logic (FAISS, embeddings, chunking)
│   │   ├── notes_service.py       # Notes-related logic
│   │   ├── progress_service.py    # Progress tracking logic
│   │   └── user_service.py        # User management and personalization
│   ├── models/                    # Database models
│   │   ├── __init__.py            # Initialize models package
│   │   ├── user.py                # User model
│   │   ├── note.py                # Notes model
│   │   ├── progress.py            # Progress model
│   │   └── chatbot_session.py     # Chat session model
│   └── utils/                     # Utility functions and helpers
│       ├── __init__.py            # Initialize utils package
│       ├── logging.py             # Centralized logging
│       ├── validation.py          # Input validation utilities
│       └── datetime_utils.py      # Date and time utilities
├── database/                      # Database and document storage
│   ├── migrations/                # Migration scripts for the database
│   ├── schema.sql                 # Initial database schema
│   ├── seed_data.sql              # Example seed data
│   ├── user_data.json             # JSON file to store user information (e.g., name)
│   ├── knowledge/                 # Markdown documents for search (RAG system)
│   └── docs/                     # Alternative markdown documents for landing pages
├── tests/                         # Unit and integration tests
│   ├── __init__.py                # Initialize tests package
│   ├── test_routes.py             # Tests for API routes
│   ├── test_services.py           # Tests for service logic
│   └── test_models.py             # Tests for database models
├── public/                        # Frontend static files
│   ├── landing.html               # Landing page (greets user, stores user name)
│   ├── playground.html            # Playground page for experimentation
│   ├── index.html                 # Main frontend interface (Sync With PAU)
│   ├── css/                       # CSS for styling (includes landing.css, playground.css, styles.css)
│   ├── js/                        # JavaScript for interactivity (e.g., scripts.js)
│   └── assets/                    # Static assets (images, icons, etc.)
├── docs/                          # Project documentation and tutorials
│   ├── architecture.md            # Architecture design document
│   ├── api_reference.md           # API reference documentation
│   ├── how_to_contribute.md       # How to contribute guide
│   ├── algorithms.md              # Details about AI algorithms used
│   └── psychology_integration.md  # Psychology and human behavior integration
└── logs/                          # Log files (git-ignored)
    └── app.log                    # Application log file
```

---

## Core Components

### 1. **`app.py`**
- **Main entry point** for the Flask application.  
- Registers API routes (chatbot, search, notes, progress, and miscellaneous endpoints for markdown files).  
- Serves static files from the `public/` directory.

### 2. **Routes (`pau/routes/`)**
- Contains modular **API endpoints** for the chatbot, search (including a RAG-based search using FAISS), notes, progress, and miscellaneous endpoints (such as serving markdown files from different directories).
- The new markdown-serving endpoints distinguish between knowledge documents (using `/api/md-knowledge/<filename>`) and landing docs (e.g., `/api/md-docs/<filename>`).

### 3. **Services (`pau/services/`)**
- Implements the core **business logic**:
  - **`ai_engine.py`** handles AI functions like memory, intuition, and emotion simulation.
  - **`search_service.py`** now includes code for chunking, embedding via a local API, building a FAISS index, and performing a retrieval-augmented search.
  - **Other services** handle notes, progress tracking, and user management.

### 4. **Models (`pau/models/`)**
- Contains database models for users, notes, progress tracking, and chatbot sessions.

### 5. **Utilities (`pau/utils/`)**
- Provides helper functions (logging, input validation, date/time utilities) used across the project.

### 6. **Database and Documents (`database/`)**
- Stores migration scripts, the initial schema, seed data, and user data.
- The **knowledge** folder contains markdown files that are automatically processed (chunked and embedded) for the FAISS search system.
- The **docs** folder is used for alternative markdown content served on landing pages.

### 7. **Tests (`tests/`)**
- Unit and integration tests ensure that routes, services, and models work as expected.

### 8. **Frontend (`public/`)**
- Contains static HTML pages: **Landing**, **Main Interface (Sync With PAU)**, and **Playground**.
- JavaScript files (e.g., `scripts.js`) handle UI interactivity, including the new search functionality.
- CSS files style the UI (including retro/terminal styles in `landing.css`).

### 9. **Documentation (`docs/`)**
- Provides detailed references on architecture, API endpoints, contribution guidelines, AI algorithms, and the integration of psychology with AI.

---

## Setup Instructions

### 1. **Prerequisites**
- Python 3.8+  
- A virtual environment tool (recommended)  
- SQLite3 (for the local database)

### 2. **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/PAU.git
   cd PAU
   ```
2. **Create and activate** a virtual environment:
   ```bash
   python -m venv venv
   # For Linux/macOS:
   source venv/bin/activate
   # For Windows:
   venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Initialize the Database**
1. **Run the schema** (assuming `database/pau.db` is your DB file):
   ```bash
   sqlite3 database/pau.db < database/schema.sql
   ```
2. (**Optional**) **Seed** the database:
   ```bash
   sqlite3 database/pau.db < database/seed_data.sql
   ```

### 4. **Build the FAISS Index (Optional)**
- Run the index-building function to process all markdown files in `database/knowledge`:
  ```python
  from pau.services.search_service import build_faiss_index
  build_faiss_index()
  ```

### 5. **(Optional) Start the Watchdog Service**
- To automatically process new or modified markdown files, run the watchdog script:
  ```bash
  python watcher.py
  ```

### 6. **Run the Application**
1. **Start** the Flask app:
   ```bash
   python app.py
   ```
2. **Open** your browser and navigate to:
   - `http://127.0.0.1:5000/` → **Landing Page** (greeting and navigation).
   - `http://127.0.0.1:5000/app` → **Main Interface** (Sync With PAU).
   - `http://127.0.0.1:5000/playground` → **Playground** (experimental features).

---

## Usage

### Landing Page
- **Greets** the user in a retro style and stores their name via API calls to update `database/user_data.json`.  
- Provides navigation to the main PAU interface or experimental Playground.

### Main Interface (Sync With PAU)
- Loads the primary application features including the chatbot.
- Enables chat functionality with context-aware memory and integration with AI functions.

### Search Functionality (RAG Search)
- **RAG Search System**:  
  Processes markdown documents in `database/knowledge` by chunking, embedding via a locally running model, and indexing with FAISS.
- When a user submits a search query, the system returns the most relevant chunks along with a link (e.g., `/api/md-knowledge/about.md`) to view the original file.

### Playground
- A space for experimental features and new ideas that can be iterated on quickly.

---

## New Features

1. **FAISS-based RAG Search**:  
   - Processes markdown documents from the knowledge folder.  
   - Embeds text using a local embedding API.  
   - Indexes chunks with FAISS and returns the most relevant results along with document links.

2. **Watchdog Integration (Optional)**:  
   - Uses the watchdog library to monitor `database/knowledge` for new or modified markdown files.  
   - Automatically rebuilds the FAISS index when changes are detected.

3. **Enhanced Markdown Serving Endpoints**:  
   - Distinct endpoints (e.g., `/api/md-knowledge/<filename>`) serve markdown files from the knowledge folder.  
   - Ensures that search result links correctly open the original markdown documents.

---

## Future Development

1. **Advanced AI Enhancements**  
   - Improve context-aware reasoning, emotional simulation, and long-term memory management.

2. **Further Frontend Development**  
   - Migrate or extend the UI using modern frontend frameworks (e.g., React or Vue) for improved interactivity.

3. **Social Media Integration**  
   - Incorporate social features such as shared progress tracking and user collaboration.

4. **Extended Logging & Monitoring**  
   - Develop real-time dashboards for performance metrics, error tracking, and user insights.

5. **Plugin Ecosystem**  
   - Allow third-party modules and custom AI plugins to extend PAU’s functionality.

---

**Let’s build PAU together and redefine personal upskilling!**

---
