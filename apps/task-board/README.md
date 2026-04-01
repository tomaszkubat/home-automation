# Family Task Board

A lightweight web application for managing family tasks using Flask and SQLite.

## Features
- View all tasks
- Add new tasks
- Edit existing tasks
- Delete tasks
- Task statuses: pending, in progress, completed

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python app.py`
3. Open your browser to `http://127.0.0.1:5000/`

## Usage
- Navigate to the home page to see all tasks.
- Click "Add Task" to create a new task.
- Click "Edit" next to a task to modify it.
- Click "Delete" to remove a task.

## Troubleshooting
- If you encounter database errors, delete `tasks.db` and restart the app to recreate the database.
- Ensure Flask is installed correctly.
