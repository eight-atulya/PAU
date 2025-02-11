# pau/routes/__init__.py
from flask import Blueprint
from .chatbot_routes import chatbot_bp
from .search_routes import search_bp
from .notes_routes import notes_bp
from .progress_routes import progress_bp
from .landing_routes import landing_bp
from .misc_routes import misc_bp


def register_routes(app):
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(landing_bp)
    app.register_blueprint(misc_bp)
    # ...
