import webbrowser
import subprocess
import platform
import os
from typing import List

class Launcher:
    """Cross-platform launcher for URLs, applications, and files."""

    @staticmethod
    def open_url(url: str):
        """Open a URL in the default browser."""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening URL {url}: {e}")
            return False

    @staticmethod
    def open_app(app_path: str):
        """Open an application."""
        try:
            system = platform.system()

            if system == "Windows":
                subprocess.Popen(app_path, shell=True)
            elif system == "Darwin":  # macOS
                subprocess.Popen(['open', '-a', app_path])
            else:  # Linux and others
                subprocess.Popen([app_path], shell=False)

            return True
        except Exception as e:
            print(f"Error opening app {app_path}: {e}")
            return False

    @staticmethod
    def open_file(file_path: str):
        """Open a file or folder with the default application."""
        try:
            system = platform.system()

            if system == "Windows":
                os.startfile(file_path)
            elif system == "Darwin":  # macOS
                subprocess.Popen(['open', file_path])
            else:  # Linux
                subprocess.Popen(['xdg-open', file_path])

            return True
        except Exception as e:
            print(f"Error opening file {file_path}: {e}")
            return False

    @staticmethod
    def launch_task(task_config: dict):
        """Launch all items in a task configuration."""
        results = {
            'urls': [],
            'apps': [],
            'files': []
        }

        # Open URLs
        for url in task_config.get('urls', []):
            success = Launcher.open_url(url)
            results['urls'].append({'url': url, 'success': success})

        # Open applications
        for app in task_config.get('apps', []):
            success = Launcher.open_app(app)
            results['apps'].append({'app': app, 'success': success})

        # Open files/folders
        for file in task_config.get('files', []):
            success = Launcher.open_file(file)
            results['files'].append({'file': file, 'success': success})

        return results
