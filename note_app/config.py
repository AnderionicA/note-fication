"""
Configuration settings for the Ultimate Note Taking App.
"""

import os

# Default settings
DEFAULT_DATA_DIR = "data"
DEFAULT_NOTES_FILE = "notes.json"
MAX_CONTENT_PREVIEW_LENGTH = 100
MAX_SEARCH_RESULTS = 50

# Application metadata
APP_NAME = "Ultimate Note Taking App"
APP_VERSION = "1.0.0"
AUTHOR = "Note Taking App Developer"

# File paths
DATA_DIR = os.environ.get("NOTE_APP_DATA_DIR", DEFAULT_DATA_DIR)
NOTES_FILE_PATH = os.path.join(DATA_DIR, DEFAULT_NOTES_FILE)

# UI settings
UI_THEME = os.environ.get("NOTE_APP_THEME", "default")
UI_COLORS = {
    "primary": "#2c3e50",
    "secondary": "#34495e",
    "accent": "#3498db",
    "success": "#2ecc71",
    "warning": "#f39c12",
    "danger": "#e74c3c"
}