from run import run
import json

def handler(request, response):
    """Vercel entrypoint for serverless function."""
    try:
        result = run()
        response.status_code = 200
        response.headers["Content-Type"] = "application/json"
        response.body = json.dumps(result)
    except Exception as e:
        response.status_code = 500
        response.body = json.dumps({"error": str(e)})
