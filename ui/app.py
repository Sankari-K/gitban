from flask import Flask, render_template, jsonify

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks')
def tasks():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
