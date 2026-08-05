from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Welcome to the Task Manager API</h1>"


@app.route("/about")
def about():
    return "<h2>This API is built using Flask.</h2>"


@app.route("/hello/<name>")
def hello(name):
    return f"<h2>Hello, {name}!</h2>"


@app.route("/square/<int:number>")
def square(number):
    return {
        "number": number,
        "square": number * number
    }


@app.route("/status")
def status():
    return {
        "status": "running",
        "message": "Task Manager API is up and running."
    }


if __name__ == "__main__":
    app.run(debug=True)