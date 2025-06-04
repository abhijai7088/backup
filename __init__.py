import os
import logging
from flask import Flask, send_from_directory
from .routes import bp as api_bp
from .extensions import mongo

def create_app():
    react_build_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../frontend/dist'))

    app = Flask(
        __name__,
        static_folder=react_build_dir,
        static_url_path='/'
    )

    # ✅ Logging setup after defining `app`
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    # Load config
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/nfc_blockchain_db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')

    # Init extensions
    mongo.init_app(app)

    # Register Blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # Serve React app
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app
