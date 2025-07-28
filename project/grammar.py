from flask import Blueprint, request, jsonify, abort
from . import services

grammar_bp = Blueprint('grammar', __name__)

@grammar_bp.route('/check-grammar', methods=['POST'])
def check_grammar():
    """Checks the grammar of the provided text."""
    if not request.json or 'text' not in request.json:
        abort(400, description="Missing 'text' in request body.")

    text = request.json['text']
    results, error = services.check_text_grammar(text)

    if error:
        abort(503, description=error)  # 503 Service Unavailable

    return jsonify(results)