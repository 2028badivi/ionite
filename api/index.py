from flask import Flask
import run   # your run.py logic

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, this is the home page!"

@app.route("/run")
def run_script():
    try:
        result = run.main()
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}", 500
