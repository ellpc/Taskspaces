import customtkinter as ctk
from config_manager import ConfigManager
from launcher import Launcher
import tkinter as tk
from tkinter import messagebox, filedialog

# Modern glass-like color scheme
COLORS = {
    'bg_primary': '#0f0f1e',
    'bg_secondary': '#1a1a2e',
    'bg_glass': '#1e1e3f',
    'accent_primary': '#6366f1',
    'accent_hover': '#4f46e5',
    'accent_secondary': '#8b5cf6',
    'text_primary': '#f1f5f9',
    'text_secondary': '#94a3b8',
    'success': '#10b981',
    'success_hover': '#059669',
    'danger': '#ef4444',
    'danger_hover': '#dc2626',
    'glass_border': '#2d2d5f'
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class GlassFrame(ctk.CTkFrame):
    """Custom frame with glass-like appearance."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color=COLORS['bg_glass'],
            border_width=1,
            border_color=COLORS['glass_border'],
            corner_radius=15,
            **kwargs
        )


class ModernButton(ctk.CTkButton):
    """Modern styled button with glass effect."""

    def __init__(self, master, **kwargs):
        # Extract custom colors if provided
        is_danger = kwargs.pop('danger', False)
        is_success = kwargs.pop('success', False)

        if is_danger:
            fg_color = COLORS['danger']
            hover_color = COLORS['danger_hover']
        elif is_success:
            fg_color = COLORS['success']
            hover_color = COLORS['success_hover']
        else:
            fg_color = kwargs.pop('fg_color', COLORS['accent_primary'])
            hover_color = kwargs.pop('hover_color', COLORS['accent_hover'])

        super().__init__(
            master,
            fg_color=fg_color,
            hover_color=hover_color,
            corner_radius=10,
            border_width=0,
            **kwargs
        )


class TaskEditDialog(ctk.CTkToplevel):
    """Dialog for editing task items (URLs, apps, files)."""

    def __init__(self, parent, task_name, config_manager, on_save_callback):
        super().__init__(parent)

        self.task_name = task_name
        self.config_manager = config_manager
        self.on_save_callback = on_save_callback

        self.title(f"Edit Task: {task_name}")
        self.geometry("750x650")
        self.resizable(True, True)
        self.configure(fg_color=COLORS['bg_primary'])

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.load_task_data()

    def create_widgets(self):
        """Create the dialog widgets."""
        # Main container
        main_frame = GlassFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Task name section
        name_frame = GlassFrame(main_frame)
        name_frame.pack(fill="x", padx=15, pady=(15, 20))

        ctk.CTkLabel(name_frame, text="Task Name:",
                    font=("Segoe UI", 14, "bold"),
                    text_color=COLORS['text_primary']).pack(side="left", padx=15, pady=12)

        self.name_entry = ctk.CTkEntry(name_frame, width=350, height=40,
                                       font=("Segoe UI", 12),
                                       fg_color=COLORS['bg_secondary'],
                                       border_color=COLORS['glass_border'])
        self.name_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.name_entry.insert(0, self.task_name)

        ModernButton(name_frame, text="Rename", command=self.rename_task,
                    width=100, height=40).pack(side="left", padx=15, pady=12)

        # Notebook for tabs
        self.tabview = ctk.CTkTabview(main_frame,
                                     fg_color=COLORS['bg_secondary'],
                                     segmented_button_fg_color=COLORS['bg_glass'],
                                     segmented_button_selected_color=COLORS['accent_primary'],
                                     segmented_button_selected_hover_color=COLORS['accent_hover'])
        self.tabview.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create tabs
        self.tabview.add("🌐 URLs")
        self.tabview.add("💻 Applications")
        self.tabview.add("📁 Files/Folders")

        # URLs tab
        self.create_item_tab(self.tabview.tab("🌐 URLs"), "urls", "URL", "https://example.com")

        # Apps tab
        self.create_item_tab(self.tabview.tab("💻 Applications"), "apps", "Application Path",
                            "/path/to/app or app.exe")

        # Files tab
        self.create_item_tab(self.tabview.tab("📁 Files/Folders"), "files", "File/Folder Path",
                            "/path/to/file", show_browse=True)

        # Bottom buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))

        ModernButton(button_frame, text="Close", command=self.destroy,
                    width=130, height=45,
                    fg_color=COLORS['bg_secondary'],
                    hover_color=COLORS['glass_border']).pack(side="right", padx=5)

        ModernButton(button_frame, text="🚀 Launch Task", command=self.launch_task,
                    width=150, height=45, success=True,
                    font=("Segoe UI", 13, "bold")).pack(side="right", padx=5)

    def create_item_tab(self, parent, item_type, label_text, placeholder, show_browse=False):
        """Create a tab for managing items (URLs, apps, or files)."""
        # Store references
        if not hasattr(self, 'item_frames'):
            self.item_frames = {}
            self.item_listboxes = {}
            self.item_entries = {}

        # Input frame
        input_frame = GlassFrame(parent)
        input_frame.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(input_frame, text=f"Add {label_text}:",
                    font=("Segoe UI", 13, "bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w", padx=15, pady=(12, 8))

        entry_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        entry_frame.pack(fill="x", padx=15, pady=(0, 12))

        entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder,
                           font=("Segoe UI", 11), height=38,
                           fg_color=COLORS['bg_secondary'],
                           border_color=COLORS['glass_border'])
        entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.item_entries[item_type] = entry

        if show_browse:
            ModernButton(entry_frame, text="📂 Browse",
                        command=lambda: self.browse_file(item_type),
                        width=100, height=38).pack(side="left", padx=4)

        ModernButton(entry_frame, text="+ Add",
                    command=lambda: self.add_item(item_type),
                    width=90, height=38).pack(side="left", padx=4)

        # List frame
        list_frame = GlassFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        ctk.CTkLabel(list_frame, text=f"Current {label_text}s:",
                    font=("Segoe UI", 12, "bold"),
                    text_color=COLORS['text_secondary']).pack(anchor="w", padx=15, pady=(12, 8))

        # Scrollable frame for items
        scroll_frame = ctk.CTkScrollableFrame(list_frame, height=220,
                                              fg_color=COLORS['bg_secondary'])
        scroll_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.item_frames[item_type] = scroll_frame

    def browse_file(self, item_type):
        """Open file browser dialog."""
        filename = filedialog.askopenfilename(parent=self, title="Select File or Folder")
        if filename:
            self.item_entries[item_type].delete(0, 'end')
            self.item_entries[item_type].insert(0, filename)

    def load_task_data(self):
        """Load task data into the dialog."""
        task = self.config_manager.get_task(self.task_name)
        if task:
            for item_type in ['urls', 'apps', 'files']:
                self.refresh_item_list(item_type)

    def refresh_item_list(self, item_type):
        """Refresh the list of items for a given type."""
        # Clear existing widgets
        for widget in self.item_frames[item_type].winfo_children():
            widget.destroy()

        # Get current task data
        task = self.config_manager.get_task(self.task_name)
        if not task:
            return

        items = task.get(item_type, [])

        if not items:
            ctk.CTkLabel(self.item_frames[item_type], text="No items added yet",
                        text_color=COLORS['text_secondary'],
                        font=("Segoe UI", 11, "italic")).pack(pady=30)
        else:
            for item in items:
                self.create_item_row(item_type, item)

    def create_item_row(self, item_type, item_value):
        """Create a row for a single item."""
        row_frame = GlassFrame(self.item_frames[item_type])
        row_frame.pack(fill="x", padx=8, pady=5)

        # Item label with text wrapping
        label = ctk.CTkLabel(row_frame, text=item_value, anchor="w",
                           font=("Segoe UI", 10),
                           text_color=COLORS['text_primary'])
        label.pack(side="left", fill="x", expand=True, padx=15, pady=10)

        # Delete button
        ModernButton(row_frame, text="Remove", width=85, height=32,
                    command=lambda: self.remove_item(item_type, item_value),
                    danger=True).pack(side="right", padx=12, pady=8)

    def add_item(self, item_type):
        """Add a new item to the task."""
        item_value = self.item_entries[item_type].get().strip()

        if not item_value:
            messagebox.showwarning("Empty Field", "Please enter a value", parent=self)
            return

        # Update current task name in case it was renamed
        current_name = self.name_entry.get().strip()

        if self.config_manager.add_item(current_name, item_type, item_value):
            self.item_entries[item_type].delete(0, 'end')
            self.refresh_item_list(item_type)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", "Failed to add item", parent=self)

    def remove_item(self, item_type, item_value):
        """Remove an item from the task."""
        current_name = self.name_entry.get().strip()

        if self.config_manager.remove_item(current_name, item_type, item_value):
            self.refresh_item_list(item_type)
            self.on_save_callback()

    def rename_task(self):
        """Rename the task."""
        new_name = self.name_entry.get().strip()

        if not new_name:
            messagebox.showwarning("Empty Name", "Task name cannot be empty", parent=self)
            return

        if new_name == self.task_name:
            return

        if self.config_manager.rename_task(self.task_name, new_name):
            self.task_name = new_name
            self.title(f"Edit Task: {new_name}")
            self.on_save_callback()
            messagebox.showinfo("Success", f"Task renamed to '{new_name}'", parent=self)
        else:
            messagebox.showerror("Error", "Task name already exists or rename failed", parent=self)

    def launch_task(self):
        """Launch the current task."""
        current_name = self.name_entry.get().strip()
        task = self.config_manager.get_task(current_name)

        if task:
            results = Launcher.launch_task(task)
            messagebox.showinfo("Task Launched", f"Launched task '{current_name}'", parent=self)


class TaskspacesApp(ctk.CTk):
    """Main application window with modern glass-like design."""

    def __init__(self):
        super().__init__()

        self.title("Taskspaces")
        self.geometry("650x750")
        self.configure(fg_color=COLORS['bg_primary'])

        self.is_pinned = False
        self.config_manager = ConfigManager()

        self.create_widgets()
        self.refresh_task_list()

    def toggle_pin(self):
        """Toggle window always-on-top state."""
        self.is_pinned = not self.is_pinned
        self.attributes('-topmost', self.is_pinned)

        # Update pin button appearance
        if self.is_pinned:
            self.pin_btn.configure(text="📌", fg_color=COLORS['accent_secondary'])
        else:
            self.pin_btn.configure(text="📌", fg_color=COLORS['bg_glass'])

    def create_widgets(self):
        """Create the main UI widgets."""
        # Main container with glass effect
        main_container = GlassFrame(self)
        main_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Header
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        # Title with gradient-like effect
        title_label = ctk.CTkLabel(header_frame, text="✨ Taskspaces",
                                   font=("Segoe UI", 32, "bold"),
                                   text_color=COLORS['text_primary'])
        title_label.pack(side="left")

        # Right side buttons
        btn_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        btn_container.pack(side="right")

        # Pin button
        self.pin_btn = ctk.CTkButton(btn_container, text="📌", width=45, height=45,
                                     command=self.toggle_pin,
                                     fg_color=COLORS['bg_glass'],
                                     hover_color=COLORS['glass_border'],
                                     corner_radius=10,
                                     font=("Segoe UI", 18))
        self.pin_btn.pack(side="left", padx=5)

        # New task button
        ModernButton(btn_container, text="+ New Task", command=self.add_task,
                    width=130, height=45,
                    font=("Segoe UI", 13, "bold")).pack(side="left", padx=5)

        # Subtitle
        subtitle = ctk.CTkLabel(main_container,
                               text="Click a task to launch all associated items",
                               font=("Segoe UI", 13),
                               text_color=COLORS['text_secondary'])
        subtitle.pack(padx=20, pady=(0, 15))

        # Scrollable frame for tasks
        self.task_container = ctk.CTkScrollableFrame(main_container,
                                                     fg_color="transparent")
        self.task_container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

    def refresh_task_list(self):
        """Refresh the list of task buttons."""
        # Clear existing widgets
        for widget in self.task_container.winfo_children():
            widget.destroy()

        tasks = self.config_manager.get_all_tasks()

        if not tasks:
            empty_frame = GlassFrame(self.task_container)
            empty_frame.pack(pady=50, padx=20, fill="x")

            no_tasks_label = ctk.CTkLabel(empty_frame,
                                         text="No tasks yet.\nClick '+ New Task' to get started!",
                                         font=("Segoe UI", 15),
                                         text_color=COLORS['text_secondary'])
            no_tasks_label.pack(pady=40)
        else:
            for task_name in tasks:
                self.create_task_button(task_name)

    def create_task_button(self, task_name):
        """Create a modern task button with glass effect."""
        task_frame = GlassFrame(self.task_container)
        task_frame.pack(fill="x", pady=10, ipady=8)

        # Main task button with gradient-like appearance
        task_btn = ctk.CTkButton(
            task_frame,
            text=task_name,
            command=lambda: self.launch_task(task_name),
            font=("Segoe UI", 18, "bold"),
            height=70,
            corner_radius=12,
            fg_color=COLORS['accent_primary'],
            hover_color=COLORS['accent_hover'],
            anchor="center"
        )
        task_btn.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=12)

        # Button frame for edit/delete
        btn_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=(0, 15))

        ModernButton(btn_frame, text="✏️ Edit", width=75, height=35,
                    command=lambda: self.edit_task(task_name),
                    fg_color=COLORS['bg_secondary'],
                    hover_color=COLORS['glass_border']).pack(pady=3)

        ModernButton(btn_frame, text="🗑️ Delete", width=75, height=35,
                    command=lambda: self.delete_task(task_name),
                    danger=True).pack(pady=3)

    def add_task(self):
        """Add a new task."""
        dialog = ctk.CTkInputDialog(text="Enter task name:", title="New Task")
        task_name = dialog.get_input()

        if task_name:
            task_name = task_name.strip()
            if self.config_manager.add_task(task_name):
                self.refresh_task_list()
                # Automatically open edit dialog for new task
                self.edit_task(task_name)
            else:
                messagebox.showerror("Error", "Task already exists or failed to create")

    def edit_task(self, task_name):
        """Edit a task."""
        TaskEditDialog(self, task_name, self.config_manager, self.refresh_task_list)

    def delete_task(self, task_name):
        """Delete a task."""
        if messagebox.askyesno("Confirm Delete", f"Delete task '{task_name}'?"):
            if self.config_manager.delete_task(task_name):
                self.refresh_task_list()

    def launch_task(self, task_name):
        """Launch all items in a task."""
        task = self.config_manager.get_task(task_name)

        if task:
            # Count total items
            total_items = len(task.get('urls', [])) + len(task.get('apps', [])) + len(task.get('files', []))

            if total_items == 0:
                messagebox.showinfo("No Items", f"Task '{task_name}' has no items configured.\nClick 'Edit' to add items.")
                return

            results = Launcher.launch_task(task)
            print(f"✅ Launched task '{task_name}'")


def main():
    app = TaskspacesApp()
    app.mainloop()


if __name__ == "__main__":
    main()
