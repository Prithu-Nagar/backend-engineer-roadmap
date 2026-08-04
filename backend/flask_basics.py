"""
Flask Basics Examples
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to Flask"


@app.route("/hello/<name>")
def hello(name):
    return f"Hello, {name}!"


@app.route("/square/<int:number>")
def square(number):
    return jsonify(
        {
            "number": number,
            "square": number * number,
        }
    )


@app.route("/user", methods=["POST"])
def create_user():

    data = request.get_json()

    return jsonify(
        {
            "message": "User created successfully",
            "user": data,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)