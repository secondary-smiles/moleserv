from enum import Enum
from urllib.parse import urlparse, ParseResult

class RequestParseError(Exception):
    pass

class RequestParseGetError(Exception):
    pass
class RequestParsePutError(Exception):
    pass
class RequestParseDelError(Exception):
    pass

class RequestMethod(Enum):
    GET=0
    PUT=1
    DEL=2

class Request:
    kind: RequestMethod
    url: ParseResult

    def __init__(self, data):
        self.parse(data)
    
    def parse(self, data):
        self.kind = self._parse_kind(data)
        match self.kind:
            case RequestMethod.GET:
                self._parse_get(data)
            case RequestMethod.PUT:
                self._parse_put(data)
            case RequestMethod.DEL:
                self._parse_del(data)

    def _parse_kind(self, data):
        kind = data.split(" ")[0].strip()
        match kind:
            case "get":
                return RequestMethod.GET
            case "put":
                return RequestMethod.PUT
            case "del":
                return RequestMethod.DEL

            case _:
                raise RequestParseError("No request headers.")

    def _parse_get(self, data):
        components = data.split(" ")
        if len(components) != 2:
            raise RequestParseGetError("get request must have exactly two parts.")

        self.url = urlparse(f"molerat://{components[1].strip()}")
 

    def _parse_put(self, data):
        pass

    def _parse_del(self, data):
        pass

    def __str__(self):
        string = "Request(\r\n\t"
        string += f"{self.kind}\r\n\t"
        string += f"{self.url}\r\n\t"
        string += "\r)"

        return string

