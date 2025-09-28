from flask import Response
import run  # this imports run.py in the root

def handler(request):
    try:
        result = run.main()
        return Response(str(result), mimetype="text/plain", status=200)
    except Exception as e:
        return Response(f"Error: {str(e)}", mimetype="text/plain", status=500)
