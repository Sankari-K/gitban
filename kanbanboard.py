import json
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from uuid import uuid4
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import time

# Define task functions
def create_id():
    return str(uuid4())

def validate_status(status):
    valid_statuses = {"To Do", "In Progress", "Done"}
    if status not in valid_statuses:
        raise ValueError(f"Invalid status: {status}. Valid statuses are: {valid_statuses}")

def validate_priority(priority):
    valid_priorities = {"Low", "Medium", "High"}
    if priority not in valid_priorities:
        raise ValueError(f"Invalid priority: {priority}. Valid priorities are: {valid_priorities}")

def create_task(name, description, status, priority="Medium", assignee=None, due_date=None):
    """Create a new task in .kanban file."""
    validate_status(status)
    validate_priority(priority)

    task = {
        "id": create_id(),
        "name": name,
        "description": description,
        "status": status,
        "priority": priority,
        "assignee": assignee,
        "dueDate": due_date,
        "createdDate": datetime.now().isoformat(),
        "updatedDate": datetime.now().isoformat(),
        "tags": [],
        "comments": [],
        "subtasks": [],
        "attachments": [],
        "progress": 0,
        "estimatedTime": None
    }

    with open(".kanban", "r+") as f:
        data = json.load(f)
        data.append(task)
        f.seek(0)
        json.dump(data, f, indent=6)

    return task

def delete_task(task_id):
    """Delete a task by its ID from the .kanban file."""
    with open(".kanban", "r+") as f:
        data = json.load(f)
        data = [task for task in data if task["id"] != task_id]
        f.seek(0)
        json.dump(data, f, indent=6)
        f.truncate()

# GUI and file watching
class KanbanFileHandler(FileSystemEventHandler):
    def __init__(self, refresh_func):
        super().__init__()
        self.refresh_func = refresh_func

    def on_modified(self, event):
        if event.src_path.endswith(".kanban"):
            self.refresh_func()

class KanbanBoard:
    def __init__(self, root):
        self.root = root
        self.task_data = self.load_tasks_from_file()
        self.status_columns = {}
        self.setup_gui()
        self.refresh_tasks()

    def load_tasks_from_file(self, filename=".kanban"):
        with open(filename, "r") as f:
            return json.load(f)

    def setup_gui(self):
        self.root.title("Kanban Board")
        self.root.geometry("1000x600")
        self.root.config(bg="#f0f0f0")

        # Setup columns for statuses
        column_info = {"To Do": "#aed6f1", "In Progress": "#f9e79f", "Done": "#a9dfbf"}
        for i, (status, color) in enumerate(column_info.items()):
            frame = tk.Frame(self.root, bg=color, width=300)
            frame.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
            tk.Label(frame, text=status, bg=color, font=("Helvetica", 16, "bold")).pack(fill="x", pady=10)
            self.status_columns[status] = frame

        # Make columns resizable
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)

        # Add button to open task creation popup
        add_task_button = tk.Button(self.root, text="Create Task", command=self.open_task_creation_popup, bg="#4CAF50", fg="white")
        add_task_button.grid(row=1, column=0, columnspan=3, pady=10)

    def open_task_creation_popup(self):
        """Open a new window for task creation."""
        popup = tk.Toplevel(self.root)
        popup.title("Create Task")
        popup.geometry("400x300")
        popup.config(bg="#f0f0f0")

        tk.Label(popup, text="Add Task", font=("Helvetica", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        # Input fields
        tk.Label(popup, text="Name:", bg="#f0f0f0").pack(anchor="w", padx=20)
        name_entry = tk.Entry(popup, width=30)
        name_entry.pack(padx=20, pady=5)

        tk.Label(popup, text="Description:", bg="#f0f0f0").pack(anchor="w", padx=20)
        desc_entry = tk.Entry(popup, width=30)
        desc_entry.pack(padx=20, pady=5)

        tk.Label(popup, text="Status:", bg="#f0f0f0").pack(anchor="w", padx=20)
        status_combo = ttk.Combobox(popup, values=["To Do", "In Progress", "Done"], state="readonly")
        status_combo.pack(padx=20, pady=5)

        tk.Label(popup, text="Priority:", bg="#f0f0f0").pack(anchor="w", padx=20)
        priority_combo = ttk.Combobox(popup, values=["Low", "Medium", "High"], state="readonly")
        priority_combo.pack(padx=20, pady=5)

        tk.Label(popup, text="Assignee:", bg="#f0f0f0").pack(anchor="w", padx=20)
        assignee_entry = tk.Entry(popup, width=30)
        assignee_entry.pack(padx=20, pady=5)

        def add_task_action():
            name = name_entry.get()
            description = desc_entry.get()
            status = status_combo.get()
            priority = priority_combo.get()
            assignee = assignee_entry.get() or None

            if name and description and status and priority:
                create_task(name, description, status, priority, assignee)
                self.refresh_tasks()
                popup.destroy()

        add_task_button = tk.Button(popup, text="Add Task", command=add_task_action, bg="#4CAF50", fg="white")
        add_task_button.pack(pady=20)

    def refresh_tasks(self):
        """Refresh the task display."""
        # Clear existing widgets
        for frame in self.status_columns.values():
            for widget in frame.winfo_children()[1:]:  # Skip header
                widget.destroy()
        # Reload tasks and display
        self.task_data = self.load_tasks_from_file()
        for task in self.task_data:
            if task["status"] in self.status_columns:
                self.create_task_widget(task, self.status_columns[task["status"]])

    def create_task_widget(self, task, parent):
        task_frame = tk.Frame(parent, bg="white", padx=10, pady=5, relief="solid", bd=1)
        task_frame.pack(fill="x", padx=10, pady=5)
        
        # Task Name
        tk.Label(task_frame, text=task["name"], font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")

        # Priority
        priority_color = "red" if task['priority'] == "High" else "orange" if task['priority'] == "Medium" else "green"
        tk.Label(task_frame, text=f"Priority: {task['priority']}", bg="white", fg=priority_color).pack(anchor="w")

        # Description
        tk.Label(task_frame, text=task["description"], bg="white", wraplength=250, justify="left").pack(anchor="w", pady=5)

        # Assignee
        assignee = task["assignee"] or "Unassigned"
        tk.Label(task_frame, text=f"Assignee: {assignee}", bg="white").pack(anchor="w")

        # Delete Button
        delete_button = tk.Button(task_frame, text="X", command=lambda t=task: self.delete_task_action(t), bg="red", fg="white", width=3)
        delete_button.pack(anchor="e", padx=10)

    def delete_task_action(self, task):
        """Handle task deletion."""
        delete_task(task["id"])
        self.refresh_tasks()

def watch_kanban_file(kanban_board):
    event_handler = KanbanFileHandler(kanban_board.refresh_tasks)
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def start_kanban_gui():
    root = tk.Tk()
    kanban_board = KanbanBoard(root)
    watcher_thread = threading.Thread(target=watch_kanban_file, args=(kanban_board,), daemon=True)
    watcher_thread.start()
    root.mainloop()

if __name__ == "__main__":
    start_kanban_gui()
