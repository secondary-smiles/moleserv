from enum import Enum
from urllib.parse import urlparse, ParseResult

class RequestParseError(Exception):
    def __init__(self, message, code: int = 40):            
        super().__init__(message)
        self.code = code

class RequestMethod(Enum):
    GET=0
    PUT=1
    DEL=2

class Request:
    kind: RequestMethod
    url: ParseResult

    length: int = 0
    hash: str = ""

    keys: dict[str, str] = {}

    def __init__(self, data):
        self.parse(data)
    
    def parse(self, data):
        self._parse_head(data)
        match self.kind:
            case RequestMethod.GET:
                pass # get is very simple
            case RequestMethod.PUT:
                self._parse_put(data)
            case RequestMethod.DEL:
                self._parse_del(data)

    def _parse_head(self, data):
        components = data.split("\r\n")[0].split(" ")
        if len(components) != 2:
            raise RequestParseError("Head line has more than one part", 30)

        match components[0]:
            case "get":
                self.kind = RequestMethod.GET
            case "put":
                self.kind = RequestMethod.PUT
            case "del":
                self.kind = RequestMethod.DEL

            case _:
                raise RequestParseError("No request headers", 30)

        self.url = urlparse(f"molerat://{components[1].strip()}")

    def _parse_put(self, data):
        fields = data.split("\r\n\r\n")[0].split("\r\n")[1:]
        fields = "\r\n".join(fields)

        kv = self.parse_kv(fields)

        for key, val in kv.items():
            match key:
                case "length":
                    self.length = int(val)
                case "hash":
                    self.hash = val
                case _:
                    raise RequestParseError("Unrecognized header key", 30)

        if (self.hash and not self.length) or (self.length and not self.hash):
            raise RequestParseError("Hash and length must both be specified", 30)

        fields = data.split("\r\n\r\n")[1].split("\r\n")
        fields = "\r\n".join(fields)

        self.keys = self.parse_kv(fields)


    def _parse_del(self, data):
        self._parse_put(data) # dels are the same as puts

    def parse_kv(self, data: str) -> dict[str, str]:
        fields = data.split("\t\r\n")

        kv = {}
        for field in fields:
            key_val = field.split(":")
            key = key_val[0]
            val = ":".join(key_val[1:])
            kv[key] = val

        return kv
        

    def __str__(self):
        string = "Request(\r\n\t"
        string += f"{self.kind}\r\n\t"
        string += f"{self.url}\r\n\t"

        string += f"{self.length}\r\n\t"
        string += f"{self.hash}\r\n\t"

        string += f"{self.keys}\r\n\t"
        string += "\r)"

        return string

