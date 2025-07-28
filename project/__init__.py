import os
from flask import Flask, jsonify

def create_app(config_object='project.config.Config'):
    """Application Factory to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Ensure the notes directory exists
    os.makedirs(app.config['NOTES_DIR'], exist_ok=True)

    # Register Blueprints
    from .notes import notes_bp
    from .grammar import grammar_bp
    app.register_blueprint(notes_bp, url_prefix='/notes')
    app.register_blueprint(grammar_bp)

    # Register custom error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": error.description}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": error.description}), 404

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({"error": "Conflict", "message": error.description}), 409

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({"error": "Service Unavailable", "message": error.description}), 503

    return app