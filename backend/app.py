"""
Task Manager API

This file contains the primary Flask application developed throughout the
Backend Engineer Roadmap.

The application is extended incrementally as new backend concepts are learned,
making it a single evolving project rather than multiple isolated examples.
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