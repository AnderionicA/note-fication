# Ultimate Note Taking App

A comprehensive note-taking application built with Python that allows you to create, organize, and search your notes efficiently.

## Features

- Create, edit, and delete notes
- Tagging system for organizing notes
- Powerful search functionality
- Pin important notes
- View all available tags
- Data persistence using JSON files
- Clean and intuitive command-line interface
- Graphical user interface (GUI) option using tkinter

## Requirements

- Python 3.7 or higher

## Installation

1. Clone or download this repository
2. Navigate to the `note_app` directory
3. Run the application using Python:

### Command Line Interface
```bash
python run.py
```

### Graphical User Interface
```bash
python gui_launcher.py
```

## Usage

The application provides two interfaces:

### Command Line Interface (CLI)
The CLI provides a simple menu-driven interface:

1. **View all notes** - Display all your notes with metadata
2. **Create new note** - Create a new note with title, content, and tags
3. **Search notes** - Find notes by keywords or tags
4. **View tags** - See all tags used across your notes
5. **Exit** - Close the application

#### Creating a Note (CLI)

When creating a note:
- Enter a title for your note
- Type your content (press Enter twice to finish)
- Add comma-separated tags (optional)

#### Searching Notes (CLI)

You can search notes by:
- Entering keywords that match titles or content
- Filtering by specific tags

### Graphical User Interface (GUI)

The GUI provides a more user-friendly experience:

1. **Left Panel**:
   - Notes list with search functionality
   - Buttons for note management (New, Delete, Refresh)

2. **Right Panel**:
   - Note editor with title, tags, and content fields
   - Save button to save changes

## Data Storage

All notes are stored in JSON format in the `data/` directory. The application automatically creates this directory and the `notes.json` file when you create your first note.

## Architecture

The application follows a clean architecture pattern:

- `Note` class: Represents a single note with metadata
- `NoteManager` class: Handles storage, retrieval, and operations on notes
- `NoteTakingApp` class: Manages the CLI user interface and application flow
- `NoteTakingGUI` class: Manages the GUI user interface

## Configuration

The application uses a configuration file (`config.py`) that allows customization of:
- Data directory location
- UI settings
- Preview length limits
- Other application settings

## Future Enhancements

Potential features for future development:
- Rich text formatting
- Export to various formats (PDF, Markdown, etc.)
- Cloud synchronization
- Password protection
- Multiple notebooks/workspaces
- Attachments support
- Dark/light theme options
- Web interface