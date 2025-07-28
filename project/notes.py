from flask import Blueprint, request, jsonify, abort, Response
from . import services

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('', methods=['POST'])
def create_note():
    """Creates a new note."""
    data = request.get_json()
    if not data or 'filename' not in data or 'content' not in data:
        abort(400, description="Request must include 'filename' and 'content'.")

    filename, content = data['filename'], data['content']

    if not filename.endswith('.md'):
        abort(400, description="Filename must end with .md")

    success, error = services.save_note_content(filename, content, overwrite=False)
    if not success:
        # Differentiate between a file conflict and other errors
        if "already exists" in error:
            abort(409, description=error)
        abort(400, description=error)

    return jsonify({"message": f"Note '{filename}' created successfully."}), 201

@notes_bp.route('', methods=['GET'])
def list_notes():
    """Lists all saved notes."""
    notes, error = services.get_all_notes()
    if error:
        abort(500, description=error)
    return jsonify(notes)

@notes_bp.route('/<string:filename>', methods=['GET'])
def get_note(filename):
    """Retrieves the raw markdown content of a note."""
    content, error = services.get_note_content(filename)
    if error:
        abort(404, description=error) if "not found" in error else abort(500, description=error)
    return Response(content, mimetype='text/markdown; charset=utf-8')

@notes_bp.route('/<string:filename>', methods=['PUT'])
def update_note(filename):
    """Updates an existing note."""
    data = request.get_json()
    if not data or 'content' not in data:
        abort(400, description="Request must include 'content'.")

    # First, check if the note exists to provide a proper 404
    _, error = services.get_note_content(filename)
    if error and "not found" in error:
        abort(404, description=f"Note '{filename}' not found.")

    success, error = services.save_note_content(filename, data['content'], overwrite=True)
    if not success:
        abort(500, description=error)

    return jsonify({"message": f"Note '{filename}' updated successfully."})

@notes_bp.route('/<string:filename>', methods=['DELETE'])
def delete_note(filename):
    """Deletes a note."""
    success, error = services.delete_note_file(filename)
    if not success:
        abort(404, description=error) if "not found" in error else abort(500, description=error)
    return Response(status=204)  # No Content

@notes_bp.route('/<string:filename>/render', methods=['GET'])
def render_note(filename):
    """Returns the HTML version of a Markdown note."""
    content, error = services.get_note_content(filename)
    if error:
        abort(404, description=error) if "not found" in error else abort(500, description=error)

    html = services.render_markdown_to_html(content)
    return Response(html, mimetype='text/html')