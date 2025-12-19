import json
import os
from typing import Dict, List, Optional

class ConfigManager:
    """Manages task configurations stored in JSON format."""

    def __init__(self, config_file: str = "taskspaces_config.json"):
        self.config_file = config_file
        self.tasks = {}
        self.load_config()

    def load_config(self):
        """Load configuration from JSON file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                self.tasks = {}
        else:
            self.tasks = self._create_default_config()
            self.save_config()

    def save_config(self):
        """Save configuration to JSON file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def _create_default_config(self) -> Dict:
        """Create a default configuration with example tasks."""
        return {
            "Example Project": {
                "urls": [
                    "https://github.com",
                    "https://stackoverflow.com"
                ],
                "apps": [],
                "files": []
            },
            "Management": {
                "urls": [
                    "https://gmail.com"
                ],
                "apps": [],
                "files": []
            }
        }

    def get_all_tasks(self) -> List[str]:
        """Get list of all task names."""
        return list(self.tasks.keys())

    def get_task(self, task_name: str) -> Optional[Dict]:
        """Get a specific task configuration."""
        return self.tasks.get(task_name)

    def add_task(self, task_name: str):
        """Add a new task."""
        if task_name not in self.tasks:
            self.tasks[task_name] = {
                "urls": [],
                "apps": [],
                "files": []
            }
            self.save_config()
            return True
        return False

    def delete_task(self, task_name: str):
        """Delete a task."""
        if task_name in self.tasks:
            del self.tasks[task_name]
            self.save_config()
            return True
        return False

    def rename_task(self, old_name: str, new_name: str):
        """Rename a task."""
        if old_name in self.tasks and new_name not in self.tasks:
            self.tasks[new_name] = self.tasks.pop(old_name)
            self.save_config()
            return True
        return False

    def add_item(self, task_name: str, item_type: str, item_value: str):
        """Add an item (url, app, or file) to a task."""
        if task_name in self.tasks and item_type in ["urls", "apps", "files"]:
            if item_value not in self.tasks[task_name][item_type]:
                self.tasks[task_name][item_type].append(item_value)
                self.save_config()
                return True
        return False

    def remove_item(self, task_name: str, item_type: str, item_value: str):
        """Remove an item from a task."""
        if task_name in self.tasks and item_type in ["urls", "apps", "files"]:
            if item_value in self.tasks[task_name][item_type]:
                self.tasks[task_name][item_type].remove(item_value)
                self.save_config()
                return True
        return False
