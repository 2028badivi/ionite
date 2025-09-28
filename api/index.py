from run import run

def handler(request, response):
    try:
        # run() prints stuff, but we'll also capture a return value
        result = run()
        if result is None:
            result = {"success": True, "message": "Run completed"}
        return response.json(result)
    except Exception as e:
        return response.json({
            "success": False,
            "error": str(e)
        })
