from flask import Flask, jsonify
from run import run

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask app running ✅"

@app.route("/run")
def trigger_run():
    result = run()
    return jsonify(result)
