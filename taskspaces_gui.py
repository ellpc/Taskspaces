import customtkinter as ctk
from config_manager import ConfigManager
from launcher import Launcher
import tkinter as tk
from tkinter import messagebox, filedialog

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TaskEditDialog(ctk.CTkToplevel):
    """Dialog for editing task items (URLs, apps, files)."""

    def __init__(self, parent, task_name, config_manager, on_save_callback):
        super().__init__(parent)

        self.task_name = task_name
        self.config_manager = config_manager
        self.on_save_callback = on_save_callback

        self.title(f"Edit Task: {task_name}")
        self.geometry("700x600")
        self.resizable(True, True)

        # Make dialog modal
        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.load_task_data()

    def create_widgets(self):
        """Create the dialog widgets."""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Task name section
        name_frame = ctk.CTkFrame(main_frame)
        name_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(name_frame, text="Task Name:", font=("Arial", 14, "bold")).pack(side="left", padx=10)
        self.name_entry = ctk.CTkEntry(name_frame, width=300, font=("Arial", 12))
        self.name_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.name_entry.insert(0, self.task_name)

        rename_btn = ctk.CTkButton(name_frame, text="Rename", command=self.rename_task, width=100)
        rename_btn.pack(side="left", padx=5)

        # Notebook for tabs
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True)

        # Create tabs
        self.tabview.add("URLs")
        self.tabview.add("Applications")
        self.tabview.add("Files/Folders")

        # URLs tab
        self.create_item_tab(self.tabview.tab("URLs"), "urls", "URL", "https://example.com")

        # Apps tab
        self.create_item_tab(self.tabview.tab("Applications"), "apps", "Application Path",
                            "/path/to/app or app.exe")

        # Files tab
        self.create_item_tab(self.tabview.tab("Files/Folders"), "files", "File/Folder Path",
                            "/path/to/file", show_browse=True)

        # Bottom buttons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(20, 0))

        ctk.CTkButton(button_frame, text="Close", command=self.destroy, width=120).pack(side="right", padx=5)
        ctk.CTkButton(button_frame, text="Launch Task", command=self.launch_task,
                     width=120, fg_color="green", hover_color="darkgreen").pack(side="right", padx=5)

    def create_item_tab(self, parent, item_type, label_text, placeholder, show_browse=False):
        """Create a tab for managing items (URLs, apps, or files)."""
        # Store references
        if not hasattr(self, 'item_frames'):
            self.item_frames = {}
            self.item_listboxes = {}
            self.item_entries = {}

        # Input frame
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text=f"Add {label_text}:", font=("Arial", 12)).pack(anchor="w", padx=5)

        entry_frame = ctk.CTkFrame(input_frame)
        entry_frame.pack(fill="x", padx=5, pady=5)

        entry = ctk.CTkEntry(entry_frame, placeholder_text=placeholder, font=("Arial", 11))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.item_entries[item_type] = entry

        if show_browse:
            ctk.CTkButton(entry_frame, text="Browse", command=lambda: self.browse_file(item_type),
                         width=80).pack(side="left", padx=2)

        ctk.CTkButton(entry_frame, text="Add", command=lambda: self.add_item(item_type),
                     width=80).pack(side="left", padx=2)

        # List frame
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(list_frame, text=f"Current {label_text}s:", font=("Arial", 12)).pack(anchor="w", padx=5)

        # Scrollable frame for items
        scroll_frame = ctk.CTkScrollableFrame(list_frame, height=250)
        scroll_frame.pack(fill="both", expand=True, padx=5, pady=5)

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
                        text_color="gray").pack(pady=20)
        else:
            for item in items:
                self.create_item_row(item_type, item)

    def create_item_row(self, item_type, item_value):
        """Create a row for a single item."""
        row_frame = ctk.CTkFrame(self.item_frames[item_type])
        row_frame.pack(fill="x", padx=5, pady=3)

        # Item label with text wrapping
        label = ctk.CTkLabel(row_frame, text=item_value, anchor="w", font=("Arial", 11))
        label.pack(side="left", fill="x", expand=True, padx=10, pady=5)

        # Delete button
        delete_btn = ctk.CTkButton(row_frame, text="Remove", width=80,
                                   command=lambda: self.remove_item(item_type, item_value),
                                   fg_color="red", hover_color="darkred")
        delete_btn.pack(side="right", padx=5)

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
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("Taskspaces")
        self.geometry("600x700")

        self.config_manager = ConfigManager()

        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        """Create the main UI widgets."""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(header_frame, text="Taskspaces",
                                   font=("Arial", 28, "bold"))
        title_label.pack(side="left")

        add_btn = ctk.CTkButton(header_frame, text="+ New Task", command=self.add_task,
                               width=120, height=35, font=("Arial", 13, "bold"))
        add_btn.pack(side="right")

        # Subtitle
        subtitle = ctk.CTkLabel(self, text="Click a task to launch all associated items",
                               font=("Arial", 12), text_color="gray")
        subtitle.pack(padx=20, pady=(0, 10))

        # Scrollable frame for tasks
        self.task_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.task_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def refresh_task_list(self):
        """Refresh the list of task buttons."""
        # Clear existing widgets
        for widget in self.task_container.winfo_children():
            widget.destroy()

        tasks = self.config_manager.get_all_tasks()

        if not tasks:
            no_tasks_label = ctk.CTkLabel(self.task_container,
                                         text="No tasks yet. Click '+ New Task' to get started!",
                                         font=("Arial", 14), text_color="gray")
            no_tasks_label.pack(pady=50)
        else:
            for task_name in tasks:
                self.create_task_button(task_name)

    def create_task_button(self, task_name):
        """Create a task button."""
        task_frame = ctk.CTkFrame(self.task_container)
        task_frame.pack(fill="x", pady=8, ipady=5)

        # Main task button
        task_btn = ctk.CTkButton(task_frame, text=task_name,
                                command=lambda: self.launch_task(task_name),
                                font=("Arial", 16, "bold"), height=60,
                                corner_radius=10)
        task_btn.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)

        # Button frame for edit/delete
        btn_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        btn_frame.pack(side="right", padx=(0, 10))

        edit_btn = ctk.CTkButton(btn_frame, text="Edit", width=60, height=30,
                                command=lambda: self.edit_task(task_name))
        edit_btn.pack(pady=2)

        delete_btn = ctk.CTkButton(btn_frame, text="Delete", width=60, height=30,
                                  command=lambda: self.delete_task(task_name),
                                  fg_color="red", hover_color="darkred")
        delete_btn.pack(pady=2)

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
            print(f"Launched task '{task_name}'")


def main():
    app = TaskspacesApp()
    app.mainloop()


if __name__ == "__main__":
    main()
