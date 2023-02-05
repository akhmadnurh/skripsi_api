from src import app

@app.route("/")
def hello_world():
    return "<p>Hello, a!</p>"
