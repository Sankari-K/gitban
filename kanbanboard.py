import tkinter as tk
from tkinter import ttk

# Sample data
data = [
    {
        "id": "d10bbd99-e56b-4d7e-9e48-3fbb5b17b033",
        "name": "Design landing page",
        "description": "Create a landing page for the upcoming product launch.",
        "status": "In Progress",
        "priority": "High",
        "assignee": "Alice",
    },
    {
        "id": "a47252fc-c8c6-4dbc-8c94-d4b1a45699df",
        "name": "Implement API",
        "description": "Develop the backend API for the app.",
        "status": "To Do",
        "priority": "Medium",
        "assignee": "Bob",
    },
    {
        "id": "e0beb0b8-a325-485c-b9c7-1b7ae8438f40",
        "name": "Write documentation",
        "description": "Document the project setup and usage.",
        "status": "Done",
        "priority": "Low",
        "assignee": None,
    }
]

# Initialize main window
root = tk.Tk()
root.title("Kanban Board")
root.geometry("900x600")

# Set up columns for statuses
status_columns = {
    "To Do": tk.Frame(root, bg="lightblue", width=300),
    "In Progress": tk.Frame(root, bg="lightyellow", width=300),
    "Done": tk.Frame(root, bg="lightgreen", width=300)
}

# Arrange columns in the main window
for i, (status, frame) in enumerate(status_columns.items()):
    frame.grid(row=0, column=i, sticky="nsew")
    tk.Label(frame, text=status, bg=frame["bg"], font=("Helvetica", 16, "bold")).pack(pady=10)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

def create_task_widget(task, parent):
    """Create a widget for a task and place it inside the appropriate status column."""
    # Main frame for task
    task_frame = tk.Frame(parent, bg="white", padx=10, pady=5, relief="raised", bd=1)
    task_frame.pack(fill="x", padx=5, pady=5)

    # Task name and priority
    name_label = tk.Label(task_frame, text=task["name"], font=("Helvetica", 12, "bold"), bg="white")
    name_label.pack(anchor="w")

    priority_label = tk.Label(task_frame, text=f"Priority: {task['priority']}", bg="white", fg="red" if task['priority'] == "High" else "black")
    priority_label.pack(anchor="w")

    # Description
    description_label = tk.Label(task_frame, text=task["description"], bg="white", wraplength=250, justify="left")
    description_label.pack(anchor="w")

    # Assignee
    assignee = task["assignee"] or "Unassigned"
    assignee_label = tk.Label(task_frame, text=f"Assignee: {assignee}", bg="white")
    assignee_label.pack(anchor="w")

# Place tasks in appropriate columns based on status
for task in data:
    status = task["status"]
    if status in status_columns:
        create_task_widget(task, status_columns[status])

# Make columns resizable
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Start the GUI event loop
root.mainloop()
