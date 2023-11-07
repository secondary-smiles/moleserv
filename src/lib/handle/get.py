from lib.req import Request
from lib.res import Response

def handle_get_request(req: Request):
    res = Response(status=10, message="Success", res_type="text/plain")
    
    res._data = f"You requested '{req.url.geturl()}'\n"

    return res
