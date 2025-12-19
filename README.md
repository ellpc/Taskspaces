# Taskspaces

A sleek, cross-platform task launcher application that allows you to create task buttons, each opening multiple applications, websites, and files with a single click.

## Overview

Taskspaces is a Python-based GUI application that helps you organize and launch your work environments quickly. Create custom task buttons for different projects or activities, and configure each to open any combination of:

- **Websites/URLs** - Open multiple web pages in your default browser
- **Applications** - Launch any installed application
- **Files/Folders** - Open documents, folders, or any file type

## Features

- Modern, sleek dark-themed UI
- Cross-platform support (Windows, macOS, Linux)
- Easy task management - add, edit, rename, delete tasks
- Configure unlimited items per task
- JSON-based configuration for easy backup and sharing
- Launch all task items with a single click

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python taskspaces_gui.py
```

### Creating Your First Task

1. Click the **"+ New Task"** button
2. Enter a task name (e.g., "Development", "Management", "Personal")
3. The edit dialog will open automatically
4. Add items to your task:
   - **URLs Tab**: Add websites (e.g., github.com, gmail.com)
   - **Applications Tab**: Add application paths or commands
   - **Files/Folders Tab**: Browse and add files or folders to open

### Managing Tasks

- **Launch a Task**: Click the large task button to open all associated items
- **Edit a Task**: Click the "Edit" button to modify items or rename the task
- **Delete a Task**: Click the "Delete" button to remove a task
- **Rename a Task**: Open the edit dialog and use the "Rename" button

### Configuration

Tasks are stored in `taskspaces_config.json` in the application directory. You can:
- Back up this file to save your configuration
- Share it with others
- Edit it manually if needed (valid JSON format required)

## Platform-Specific Notes

### Windows
- Application paths: Use full paths (e.g., `C:\Program Files\App\app.exe`) or just the executable name if it's in PATH
- For Microsoft Store apps, use the app name or protocol (e.g., `ms-settings:`)

### macOS
- Application paths: Use app names (e.g., `Safari`, `Visual Studio Code`) or full paths to .app bundles

### Linux
- Application paths: Use command names (e.g., `firefox`, `code`) or full paths to executables

## Example Configuration

Here's a sample task configuration:

```json
{
    "Development": {
        "urls": [
            "https://github.com",
            "https://stackoverflow.com"
        ],
        "apps": [
            "code",
            "slack"
        ],
        "files": [
            "/home/user/projects"
        ]
    },
    "Management": {
        "urls": [
            "https://gmail.com",
            "https://calendar.google.com"
        ],
        "apps": [],
        "files": [
            "/home/user/Documents/reports"
        ]
    }
}
```

## Troubleshooting

**Issue**: Application won't launch
- Verify the application is installed and the path is correct
- On Linux, ensure the application is in your PATH or use the full path

**Issue**: URLs not opening
- Check your default browser is set correctly
- URLs without http:// or https:// will automatically have https:// prepended

**Issue**: Files/folders won't open
- Verify the path exists and you have permissions to access it
- Use absolute paths for reliability

## Legacy PowerShell Script

The original PowerShell script is available in the `Taskspaces` file for reference. The new Python application provides the same functionality with a modern GUI interface. 
