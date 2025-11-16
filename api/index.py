from flask import Flask, jsonify, request
from run import run
import os
app = Flask(__name__)


@app.route("/", methods=["GET"])
def index_get():
    try:
        result = run(
            spreadsheet_url=os.environ.get("spreadsheet"),
            recipient_email=os.environ.get("RECIPIENT_EMAIL")
        )
        return jsonify({"success": True, "result": str(result)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@app.route("/", methods=["POST"])
def index_post():
    try:
        recipient_email = request.headers.get("RECIPIENT_EMAIL")
        spreadsheet_url = request.headers.get("SPREADSHEET_URL")

        if not recipient_email or not spreadsheet_url:
            return jsonify({"success": False, "error": "Missing RECIPIENT_EMAIL or SPREADSHEET_URL"}), 400

        result = run(spreadsheet_url, recipient_email)
        return jsonify({"success": True, "result": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



# from flask import Flask, jsonify
# from run import run

# app = Flask(__name__)

# @app.route("/", methods=["GET"])
# def index():
#     try:
#         result = run()
#         return jsonify({"success": True, "result": str(result)})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500
