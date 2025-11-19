#!/usr/bin/env python3
"""
Ultimate Note Taking App
A comprehensive note-taking application with features like:
- Create, edit, delete notes
- Tagging system
- Search functionality
- Export capabilities
- Rich text support
- Multiple storage options
"""

import os
import sys
import json
import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional

# Import configuration
from config import MAX_CONTENT_PREVIEW_LENGTH


@dataclass
class Note:
    """Represents a single note with metadata."""
    id: str
    title: str
    content: str
    tags: List[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    is_pinned: bool = False
    is_archived: bool = False

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.datetime.fromisoformat(self.updated_at)


class NoteManager:
    """Manages notes storage, retrieval, and operations."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.notes_file = os.path.join(data_dir, "notes.json")
        self.notes: List[Note] = []
        self._ensure_data_dir()
        self.load_notes()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_notes(self):
        """Save all notes to the JSON file."""
        notes_data = []
        for note in self.notes:
            note_dict = {
                'id': note.id,
                'title': note.title,
                'content': note.content,
                'tags': note.tags,
                'created_at': note.created_at.isoformat(),
                'updated_at': note.updated_at.isoformat(),
                'is_pinned': note.is_pinned,
                'is_archived': note.is_archived
            }
            notes_data.append(note_dict)
        
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump(notes_data, f, indent=2)
    
    def load_notes(self):
        """Load notes from the JSON file."""
        if not os.path.exists(self.notes_file):
            self.notes = []
            return
        
        try:
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
            
            self.notes = []
            for note_data in notes_data:
                note = Note(
                    id=note_data['id'],
                    title=note_data['title'],
                    content=note_data['content'],
                    tags=note_data['tags'],
                    created_at=note_data['created_at'],
                    updated_at=note_data['updated_at'],
                    is_pinned=note_data['is_pinned'],
                    is_archived=note_data['is_archived']
                )
                self.notes.append(note)
        except (json.JSONDecodeError, KeyError):
            self.notes = []
    
    def create_note(self, title: str, content: str, tags: List[str] = None) -> Note:
        """Create a new note."""
        if tags is None:
            tags = []
        
        note_id = f"note_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        note = Note(
            id=note_id,
            title=title,
            content=content,
            tags=tags,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        
        self.notes.append(note)
        self.save_notes()
        return note
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """Get a note by ID."""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None
    
    def update_note(self, note_id: str, title: str = None, content: str = None, 
                    tags: List[str] = None, is_pinned: bool = None, is_archived: bool = None) -> bool:
        """Update a note."""
        note = self.get_note(note_id)
        if not note:
            return False
        
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if tags is not None:
            note.tags = tags
        if is_pinned is not None:
            note.is_pinned = is_pinned
        if is_archived is not None:
            note.is_archived = is_archived
        
        note.updated_at = datetime.datetime.now()
        self.save_notes()
        return True
    
    def delete_note(self, note_id: str) -> bool:
        """Delete a note."""
        note = self.get_note(note_id)
        if not note:
            return False
        
        self.notes.remove(note)
        self.save_notes()
        return True
    
    def search_notes(self, query: str = "", tags: List[str] = None, 
                     include_archived: bool = False) -> List[Note]:
        """Search notes by query and/or tags."""
        results = []
        
        for note in self.notes:
            if not include_archived and note.is_archived:
                continue
            
            # Check if query matches title or content
            matches_query = not query or query.lower() in note.title.lower() or query.lower() in note.content.lower()
            
            # Check if all tags match
            matches_tags = True
            if tags:
                note_tags_lower = [tag.lower() for tag in note.tags]
                for tag in tags:
                    if tag.lower() not in note_tags_lower:
                        matches_tags = False
                        break
            
            if matches_query and matches_tags:
                results.append(note)
        
        # Sort by pinned first, then by updated date
        results.sort(key=lambda x: (not x.is_pinned, x.updated_at), reverse=True)
        return results
    
    def get_all_tags(self) -> List[str]:
        """Get all unique tags."""
        all_tags = set()
        for note in self.notes:
            for tag in note.tags:
                all_tags.add(tag.lower())
        return sorted(list(all_tags))


class NoteTakingApp:
    """Main application class."""
    
    def __init__(self):
        self.note_manager = NoteManager()
        self.current_view = "main_menu"
    
    def run(self):
        """Run the application."""
        print("Welcome to the Ultimate Note Taking App!")
        print("=" * 40)
        
        while True:
            if self.current_view == "main_menu":
                self.show_main_menu()
            elif self.current_view == "list_notes":
                self.list_notes()
            elif self.current_view == "create_note":
                self.create_note()
            elif self.current_view == "search_notes":
                self.search_notes()
    
    def show_main_menu(self):
        """Display the main menu."""
        print("\nMain Menu:")
        print("1. View all notes")
        print("2. Create new note")
        print("3. Search notes")
        print("4. View tags")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            self.current_view = "list_notes"
        elif choice == "2":
            self.current_view = "create_note"
        elif choice == "3":
            self.current_view = "search_notes"
        elif choice == "4":
            self.view_tags()
        elif choice == "5":
            print("Thank you for using the Ultimate Note Taking App!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1-5.")
    
    def list_notes(self):
        """List all notes."""
        print("\nAll Notes:")
        print("-" * 40)
        
        notes = self.note_manager.search_notes(include_archived=False)
        
        if not notes:
            print("No notes found.")
        else:
            for i, note in enumerate(notes, 1):
                status = "PINNED" if note.is_pinned else "      "
                print(f"{i}. [{status}] {note.title} ({len(note.content)} chars)")
                print(f"   Tags: {', '.join(note.tags) if note.tags else 'None'}")
                print(f"   Updated: {note.updated_at.strftime('%Y-%m-%d %H:%M')}")
                print()
        
        input("Press Enter to return to main menu...")
        self.current_view = "main_menu"
    
    def create_note(self):
        """Create a new note."""
        print("\nCreate New Note:")
        print("-" * 20)
        
        title = input("Enter title: ").strip()
        if not title:
            print("Title cannot be empty!")
            input("Press Enter to return...")
            self.current_view = "main_menu"
            return
        
        print("Enter content (press Enter twice to finish):")
        lines = []
        empty_line_count = 0
        while True:
            line = input()
            if line == "":
                empty_line_count += 1
                if empty_line_count >= 2:
                    break
                lines.append("")
            else:
                empty_line_count = 0
                lines.append(line)
        
        content = "\n".join(lines[:-1])  # Remove the last empty line
        
        tags_input = input("Enter tags (comma-separated): ").strip()
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        note = self.note_manager.create_note(title, content, tags)
        print(f"Note '{note.title}' created successfully!")
        
        input("Press Enter to return to main menu...")
        self.current_view = "main_menu"
    
    def search_notes(self):
        """Search for notes."""
        print("\nSearch Notes:")
        print("-" * 15)
        
        query = input("Enter search query (or press Enter to skip): ").strip()
        tags_input = input("Enter tags to filter (comma-separated, or press Enter to skip): ").strip()
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else None
        
        results = self.note_manager.search_notes(query=query, tags=tags, include_archived=False)
        
        print(f"\nSearch Results ({len(results)} found):")
        print("-" * 40)
        
        if not results:
            print("No notes found matching your criteria.")
        else:
            for i, note in enumerate(results, 1):
                status = "PINNED" if note.is_pinned else "      "
                print(f"{i}. [{status}] {note.title}")
                print(f"   Tags: {', '.join(note.tags) if note.tags else 'None'}")
                print(f"   Content preview: {note.content[:MAX_CONTENT_PREVIEW_LENGTH]}{'...' if len(note.content) > MAX_CONTENT_PREVIEW_LENGTH else ''}")
                print()
        
        input("Press Enter to return to main menu...")
        self.current_view = "main_menu"
    
    def view_tags(self):
        """View all available tags."""
        tags = self.note_manager.get_all_tags()
        
        print("\nAll Tags:")
        print("-" * 10)
        
        if not tags:
            print("No tags available.")
        else:
            for i, tag in enumerate(tags, 1):
                print(f"{i}. {tag}")
        
        input("\nPress Enter to return to main menu...")
        self.current_view = "main_menu"


def main():
    """Main entry point."""
    app = NoteTakingApp()
    app.run()


if __name__ == "__main__":
    main()