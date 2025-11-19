"""
GUI interface for the Ultimate Note Taking App using tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from main import NoteManager
import datetime


class NoteTakingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Note Taking App")
        self.root.geometry("800x600")
        
        self.note_manager = NoteManager()
        self.current_note_id = None
        
        self.setup_ui()
        self.refresh_notes_list()
    
    def setup_ui(self):
        # Create main frames
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame - Notes list
        ttk.Label(left_frame, text="Notes", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Search and filter
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        ttk.Entry(search_frame, textvariable=self.search_var, width=20).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        
        # Notes listbox
        self.notes_listbox = tk.Listbox(left_frame, width=30, height=20)
        self.notes_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.notes_listbox.bind('<<ListboxSelect>>', self.on_note_select)
        
        # Buttons for note management
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="New Note", command=self.new_note).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Delete Note", command=self.delete_note).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_notes_list).pack(fill=tk.X, pady=2)
        
        # Right frame - Note editor
        ttk.Label(right_frame, text="Edit Note", font=("Arial", 12, "bold")).pack(anchor=tk.W)
        
        # Title
        title_frame = ttk.Frame(right_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(title_frame, text="Title:").pack(anchor=tk.W)
        self.title_var = tk.StringVar()
        ttk.Entry(title_frame, textvariable=self.title_var, width=50).pack(fill=tk.X)
        
        # Tags
        tags_frame = ttk.Frame(right_frame)
        tags_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(tags_frame, text="Tags (comma-separated):").pack(anchor=tk.W)
        self.tags_var = tk.StringVar()
        ttk.Entry(tags_frame, textvariable=self.tags_var, width=50).pack(fill=tk.X)
        
        # Content
        ttk.Label(right_frame, text="Content:").pack(anchor=tk.W)
        self.content_text = scrolledtext.ScrolledText(right_frame, height=20)
        self.content_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Save button
        ttk.Button(right_frame, text="Save Note", command=self.save_note).pack()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def refresh_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        
        # Get search query
        search_query = self.search_var.get().lower()
        
        # Get all notes
        all_notes = self.note_manager.search_notes()
        
        # Filter based on search query
        filtered_notes = []
        for note in all_notes:
            if (search_query in note.title.lower() or 
                search_query in note.content.lower() or
                any(search_query in tag.lower() for tag in note.tags)):
                filtered_notes.append(note)
        
        # Add to listbox
        for note in filtered_notes:
            display_text = f"[{'PINNED' if note.is_pinned else '     '}] {note.title}"
            self.notes_listbox.insert(tk.END, display_text)
        
        # Store the actual notes in the same order as displayed
        self.displayed_notes = filtered_notes
    
    def on_search_change(self, *args):
        self.refresh_notes_list()
    
    def on_note_select(self, event):
        if not self.notes_listbox.curselection():
            return
            
        index = self.notes_listbox.curselection()[0]
        selected_note = self.displayed_notes[index]
        
        self.current_note_id = selected_note.id
        self.title_var.set(selected_note.title)
        self.tags_var.set(", ".join(selected_note.tags))
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(1.0, selected_note.content)
        
        self.status_var.set(f"Editing note: {selected_note.title}")
    
    def new_note(self):
        # Clear current note
        self.current_note_id = None
        self.title_var.set("")
        self.tags_var.set("")
        self.content_text.delete(1.0, tk.END)
        
        self.status_var.set("Creating new note")
    
    def save_note(self):
        title = self.title_var.get().strip()
        content = self.content_text.get(1.0, tk.END).strip()
        tags_str = self.tags_var.get().strip()
        tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
        
        if not title:
            messagebox.showerror("Error", "Note title cannot be empty!")
            return
        
        if self.current_note_id:
            # Update existing note
            success = self.note_manager.update_note(
                self.current_note_id,
                title=title,
                content=content,
                tags=tags
            )
            if success:
                messagebox.showinfo("Success", "Note updated successfully!")
                self.status_var.set(f"Updated note: {title}")
            else:
                messagebox.showerror("Error", "Failed to update note!")
        else:
            # Create new note
            note = self.note_manager.create_note(title, content, tags)
            self.current_note_id = note.id
            messagebox.showinfo("Success", "Note created successfully!")
            self.status_var.set(f"Created note: {title}")
        
        self.refresh_notes_list()
    
    def delete_note(self):
        if not self.current_note_id:
            messagebox.showwarning("Warning", "Please select a note to delete!")
            return
        
        # Find the note to get its title for confirmation
        note = self.note_manager.get_note(self.current_note_id)
        if not note:
            messagebox.showerror("Error", "Note not found!")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{note.title}'?")
        if confirm:
            success = self.note_manager.delete_note(self.current_note_id)
            if success:
                messagebox.showinfo("Success", "Note deleted successfully!")
                self.new_note()  # Clear the editor
                self.refresh_notes_list()
                self.status_var.set("Note deleted")
            else:
                messagebox.showerror("Error", "Failed to delete note!")
    
    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = NoteTakingGUI(root)
    app.run()


if __name__ == "__main__":
    main()