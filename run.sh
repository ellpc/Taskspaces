#!/bin/bash
# Taskspaces launcher script

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import customtkinter" &> /dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Launch the application
python3 taskspaces_gui.py
