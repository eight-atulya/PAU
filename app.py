import os
from flask import Flask, send_from_directory
from pau.routes import register_routes
from pau.services.search_service import build_faiss_index
import threading
from pau.services.screen_capture import take_screenshots
from pau.services.advanced_memory import init_advanced_memory, persist_advanced_memory
from pau.services.advanced_memory import store_advanced_memory
from pau.services.ocr_llm_pipeline import pipeline_ocr_and_llm

from pau.services.ocr_llm_pipeline import process_image_directory

process_image_directory(
    directory_path="data/screen_snapshot",
    processed_log="data/processed_images.json",
    model="llama-3.2-1b-instruct"
)



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

    

def start_digitalvision_service():
    # Run the screenshot service in a background thread.
    thread = threading.Thread(
        target=take_screenshots,
        kwargs={
            "save_folder": "data/screen_snapshot",
            "prefix": "DigitalVision",
            "interval": 10,
            "iterations": 0
        },
        daemon=True
    )
    thread.start()
    print("DigitalVision service started.")



if __name__ == '__main__':
    # call init to load existing data if any
    init_advanced_memory()
    build_faiss_index()
    start_digitalvision_service()
    application = create_app()
    application.run(host='0.0.0.0', port=5000, debug=True)
