# app.py

import os
from flask import Flask, send_from_directory
from pau.routes import register_routes


def create_app():
    app = Flask(__name__)

    # -- Register your routes --
    register_routes(app)

    # -- Serve the frontend --
    @app.route('/')
    def serve_index():
        # The 'public' folder is next to this file
        return send_from_directory(os.path.join(os.path.dirname(__file__), 'public'), 'index.html')

    @app.route('/<path:filename>')
    def serve_static(filename):
        # Serve other static files (CSS, JS, images) from public/
        return send_from_directory(os.path.join(os.path.dirname(__file__), 'public'), filename)

    return app


if __name__ == '__main__':
    # Create the Flask application
    application = create_app()

    # You can set host='0.0.0.0' to listen externally
    application.run(host='0.0.0.0', port=5000, debug=True)
