# api/index.py
from flask import Flask, jsonify
from run import run

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    try:
        result = run()
        if result is None:
            result = {"success": True, "message": "Run completed"}
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
