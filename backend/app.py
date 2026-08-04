"""
Task Manager API
Main Flask Application
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {
            "message": "Task Manager API",
            "status": "Running",
            "version": "1.0.0",
        }
    )


@app.route("/health")
def health():
    return jsonify(
        {
            "status": "Healthy"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)