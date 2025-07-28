import os
import markdown
import language_tool_python
from flask import current_app

# --- Grammar Service ---
_tool = None

def get_grammar_tool():
    """Initializes and returns a singleton grammar tool instance."""
    global _tool
    if _tool is None:
        try:
            # Using 'en-US' for American English grammar rules
            _tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            # In a real app, you'd use proper logging (e.g., app.logger.error)
            print(f"Could not initialize language tool: {e}")
            _tool = None  # Ensure it stays None on failure
    return _tool

def check_text_grammar(text):
    """Checks grammar for a given text and returns results or an error."""
    tool = get_grammar_tool()
    if not tool:
        return None, "Grammar check service is not available."

    matches = tool.check(text)
    results = [
        {
            "message": match.message,
            "replacements": match.replacements,
            "offset": match.offset,
            "length": match.errorLength,
            "ruleId": match.ruleId,
        } for match in matches
    ]
    return results, None

# --- Notes Service ---

def get_notes_dir():
    """Returns the configured notes directory from the app context."""
    return current_app.config['NOTES_DIR']

def _get_note_path(filename):
    """Constructs and validates a note's file path to prevent directory traversal."""
    if os.path.basename(filename) != filename:
        return None, "Invalid filename."
    return os.path.join(get_notes_dir(), filename), None

def save_note_content(filename, content, overwrite=False):
    """Saves content to a note file."""
    file_path, err = _get_note_path(filename)
    if err:
        return False, err

    if not overwrite and os.path.exists(file_path):
        return False, f"Note '{filename}' already exists."

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, None
    except IOError as e:
        return False, f"Could not save note: {e}"

def get_all_notes():
    """Lists all note filenames."""
    notes_dir = get_notes_dir()
    try:
        if not os.path.exists(notes_dir):
            return [], None
        notes = [f for f in os.listdir(notes_dir) if f.endswith('.md') and os.path.isfile(os.path.join(notes_dir, f))]
        return notes, None
    except OSError as e:
        return None, f"Could not list notes: {e}"

def get_note_content(filename):
    """Reads the raw content of a note."""
    file_path, err = _get_note_path(filename)
    if err:
        return None, err

    if not os.path.exists(file_path):
        return None, f"Note '{filename}' not found."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read(), None
    except IOError as e:
        return None, f"Could not read note: {e}"

def delete_note_file(filename):
    """Deletes a note file."""
    file_path, err = _get_note_path(filename)
    if err:
        return False, err

    if not os.path.exists(file_path):
        return False, f"Note '{filename}' not found."

    try:
        os.remove(file_path)
        return True, None
    except OSError as e:
        return False, f"Could not delete note: {e}"

def render_markdown_to_html(markdown_content):
    """Renders a markdown string to an HTML string."""
    return markdown.markdown(markdown_content)