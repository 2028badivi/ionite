from flask import Flask, jsonify
from run import run

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    try:
        result = run()
        return jsonify({"success": True, "result": str(result)})
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
