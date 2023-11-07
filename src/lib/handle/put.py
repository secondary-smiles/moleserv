from lib.req import Request
from lib.res import Response

def handle_put_request(req: Request):
    res = Response(11, "Success")

    if req.keys:
        res.keys = req.keys
    
    return res
