
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
7. [Future Development](#future-development)

---

## Introduction

**PAU** is an open-source framework designed to build personal upskilling assistants. It integrates AI features like memory, intuition, and emotion simulation with data logging and user interaction insights. The framework is modular, scalable, and built with long-term growth in mind, supporting both developers and end-users.

Recent additions include a **Landing Page** at the root (`/`) that greets users, stores their names in a JSON file, and provides quick navigation to either **Sync With PAU** (the main application) or a **Playground** page for experimentation.

---

## Project Goals

1. **Open Framework**: A reusable base for developers to create personal assistants.  
2. **Human-Centric AI**: Integrate psychology-driven algorithms for realistic interactions.  
3. **Scalability**: Support modular growth and integration of new features like social media.  
4. **Transparency**: Log all activities for user monitoring and AI synchronization.  
5. **Extensibility**: Allow the addition of custom AI functions (e.g., memory, intuition).

---

## Directory Structure

```plaintext
PAU/
├── README.md                      # Comprehensive project documentation
├── LICENSE                        # License for open-source use
├── CONTRIBUTING.md                # Guidelines for contributing to the project
├── app.py                         # Main entry point for the backend application
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables for sensitive configs
├── pau/                           # Main backend application package
│   ├── __init__.py                # Initialize the application package
│   ├── config.py                  # Configuration settings for the app
│   ├── routes/                    # API routes (modular and extendable)
│   │   ├── __init__.py            # Register API blueprints
│   │   ├── chatbot_routes.py      # Chatbot-related API endpoints
│   │   ├── search_routes.py       # Search-related API endpoints
│   │   ├── notes_routes.py        # Notes-related API endpoints
│   │   └── progress_routes.py     # Progress tracking endpoints
│   ├── services/                  # Core business logic and services
│   │   ├── __init__.py            # Initialize services package
│   │   ├── ai_engine.py           # AI functions (e.g., memory, intuition, emotion)
│   │   ├── search_service.py      # Search-related logic
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
├── database/                      # Database and migrations
│   ├── migrations/                # Migration scripts for the database
│   ├── schema.sql                 # Initial database schema
│   ├── seed_data.sql              # Example seed data
│   └── user_data.json             # JSON file to store user information (e.g., name)
├── tests/                         # Unit and integration tests
│   ├── __init__.py                # Initialize tests package
│   ├── test_routes.py             # Tests for API routes
│   ├── test_services.py           # Tests for service logic
│   └── test_models.py             # Tests for database models
├── public/                        # Frontend static files
│   ├── landing.html               # Landing page (greets user, stores user name)
│   ├── playground.html            # Playground page for experimentation
│   ├── index.html                 # Main frontend interface (Sync With PAU)
│   ├── css/                       # CSS for styling
│   │   ├── styles.css             # General or shared styles
│   │   ├── landing.css            # Retro/terminal styles for landing page
│   │   └── playground.css         # Styles for playground page
│   ├── js/                        # JavaScript for interactivity
│   │   └── scripts.js
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
- Registers routes and serves HTML pages from the `public/` directory.  
- **Default route** (`/`) loads `landing.html` to greet the user and store their name.  
- **`/app`** serves `index.html` (the main interface).  
- **`/playground`** serves a new experimental page.

### 2. **`pau/routes/`**
- Collection of **API endpoints** for Chatbot, Notes, Search, etc.
- Includes new endpoints for **saving and retrieving user data** from `user_data.json` (if you’ve added them in a `landing_routes.py`).

### 3. **Services (`pau/services/`)**
- Encapsulates **core business logic** (e.g., AI engine, search, notes, user services).

### 4. **Models (`pau/models/`)**
- Database models for structured data.

### 5. **Utilities (`pau/utils/`)**
- Helper functions for logging, validation, date/time, etc.

### 6. **Database (`database/`)**
- **`user_data.json`** to store or retrieve user names for the landing page.  
- **Schema** and **seed** files for migrations and sample data.

### 7. **Tests (`tests/`)**
- **Unit** and **integration** tests covering routes, services, and models.

### 8. **Frontend (`public/`)**
- **`landing.html`** (new greeting page).  
- **`playground.html`** (new experimental page).  
- **`index.html`** for the main PAU interface.  
- **`css/`** for styling (including `landing.css` or `playground.css` for a retro vibe).  
- **`js/`** for interactivity.

### 9. **Documentation (`docs/`)**
- In-depth references on architecture, APIs, contribution guidelines, and more.

---

## Setup Instructions

### 1. **Prerequisites**
- Python 3.8+  
- Virtual environment tool (recommended)  
- SQLite3 (for local database usage)

### 2. **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/PAU.git
   cd PAU
   ```
2. **Create and activate** a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Initialize the Database**
1. **Run schema** (assuming `database/pau.db` is your DB file):
   ```bash
   sqlite3 database/pau.db < database/schema.sql
   ```
2. (**Optional**) **Seed** the database:
   ```bash
   sqlite3 database/pau.db < database/seed_data.sql
   ```

### 4. **Run the Application**
1. **Start** the Flask app:
   ```bash
   python app.py
   ```
2. **Open** your browser and navigate to:
   - `http://127.0.0.1:5000/` → Lands on the new **Landing Page** with greeting & user name storage.
   - `http://127.0.0.1:5000/app` → Loads the existing **main interface** (`index.html`).
   - `http://127.0.0.1:5000/playground` → Loads the **Playground** page (currently experimental).

---

## Usage

1. **Landing Page**  
   - **Greets** the user in a retro style (if using `landing.css`).  
   - **Stores** the user’s name in `database/user_data.json` via API endpoints.  
   - Provides **buttons** to go to the main PAU app or the Playground.

2. **Sync With PAU**  
   - Redirects to `http://127.0.0.1:5000/app`, serving `index.html`.  
   - Continue using the existing AI or upskilling functionality.

3. **Playground**  
   - A **placeholder** page (`playground.html`) for experimental features.  
   - Currently contains dummy text, but you can extend it with new ideas.

---

## Future Development

1. **AI Enhancements**  
   - Add advanced context-aware reasoning, emotional simulation, and long-term memory capabilities.  

2. **Further Frontend Development**  
   - Migrate or expand the UI with a robust frontend framework (React, Vue, etc.).  
   - Enhance the **Landing** and **Playground** pages with dynamic content and improved styles.

3. **Social Media Platform Integration**  
   - Allow shared progress tracking, user collaboration, and skill endorsements.

4. **Extended Logging & Monitoring**  
   - Real-time dashboards for user insights, performance metrics, and error tracking.

5. **Plugin Ecosystem**  
   - Build modular plugins for specialized AI tasks or third-party integrations.

---

**Let’s build PAU together and redefine personal upskilling!**

