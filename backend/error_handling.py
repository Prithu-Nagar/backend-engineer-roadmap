from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    if task_id <= 0:
        return jsonify({"error": "Invalid task ID"}), 400

    if task_id != 1:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(
        {
            "id": 1,
            "title": "Learn Flask",
            "completed": False,
        }
    ), 200


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def handle_internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True)