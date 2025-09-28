from run import run

def handler(request, response):
    try:
        result = run()
        return response.json(result)
    except Exception as e:
        return response.json({"success": False, "error": str(e)})
