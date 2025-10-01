from flask import Flask, jsonify, request
from run import run

app = Flask(__name__)

@app.route("/", methods=["POST"])
def index():
    try:
        # Get the JSON data from the request body
        data = request.get_json()
        
        # Check if data was received and contains all necessary keys
        if not data:
            return jsonify({"success": False, "error": "No JSON data received."}), 400
        
        required_keys = ["google_service_account_json", "ion_sessionid", "sender_email", "sender_password", "recipient_email"]
        if not all(key in data for key in required_keys):
            return jsonify({"success": False, "error": "Missing required data in JSON payload."}), 400
            
        # Pass all arguments from the JSON payload to the run() function
        result = run(
            google_service_account_json=data.get("google_service_account_json"),
            ion_sessionid=data.get("ion_sessionid"),
            sender_email=data.get("sender_email"),
            sender_password=data.get("sender_password"),
            recipient_email=data.get("recipient_email")
        )
        
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
