# Markdown Note-Taking API

import os

class Config:
    """Base configuration."""
    # Use an absolute path for the notes directory relative to the project root
    NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'notes')
    TESTING = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    # Use a separate directory for test notes to avoid conflicts
    NOTES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'tests', 'test_notes')