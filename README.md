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
