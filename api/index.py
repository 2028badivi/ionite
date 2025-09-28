from run import run

def handler(request):
    try:
        result = run()
        if result is None:
            result = {"success": True, "message": "Run completed"}
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": result
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": {"success": False, "error": str(e)}
        }
