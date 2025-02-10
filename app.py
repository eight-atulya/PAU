import os
from flask import Flask, send_from_directory
from pau.routes import register_routes

def create_app():
    app = Flask(__name__)

    # Register your existing routes/blueprints
    register_routes(app)

    # 1. Serve the landing page at '/'
    @app.route('/')
    def serve_landing():
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), 'public'),
            'landing.html'
        )

    # 2. Serve the main app (old "index.html") at '/app'
    @app.route('/app')
    def serve_index():
        return send_from_directory(
            os.path.join(os.path.dirname(__file__), 'public'),
            'index.html'
        )


    # 4. Catch-all route for any static file references (CSS, JS, images, etc.)
    @app.route('/<path:filename>')
    def serve_static(filename):
        return send_from_directory(os.path.join(os.path.dirname(__file__), 'public'), filename)

    return app

if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000, debug=True)
