from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data
tasks = [
    {
        "id": 1,
        "title": "Learn Flask",
        "description": "Build a CRUD REST API",
        "completed": False
    },
    {
        "id": 2,
        "title": "Test API",
        "description": "Test the API using Postman",
        "completed": False
    }
]

# Keep track of the next available ID
next_id = 3


# GET /tasks
# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# GET /tasks/<id>
# Get one task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):

    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task), 200

    return jsonify({
        "error": "Task not found"
    }), 404


# POST /tasks
# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():

    global next_id

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "title" not in data:
        return jsonify({
            "error": "Title is required"
        }), 400

    new_task = {
        "id": next_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": data.get("completed", False)
    }

    tasks.append(new_task)

    next_id += 1

    return jsonify(new_task), 201


# PUT /tasks/<id>
# Update a task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    for task in tasks:

        if task["id"] == task_id:

            if "title" in data:
                task["title"] = data["title"]

            if "description" in data:
                task["description"] = data["description"]

            if "completed" in data:
                task["completed"] = data["completed"]

            return jsonify(task), 200

    return jsonify({
        "error": "Task not found"
    }), 404


# DELETE /tasks/<id>
# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    for task in tasks:

        if task["id"] == task_id:

            tasks.remove(task)

            return jsonify({
                "message": "Task deleted successfully"
            }), 200

    return jsonify({
        "error": "Task not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)