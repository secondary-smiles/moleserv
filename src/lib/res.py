import hashlib

class ResponseError(Exception):
    pass

class Response:
    status: int = 10
    message: str = ""
    res_type: str = ""
    len: int
    hash: str

    keys: dict[str, str]
    _data: str

    def __init__(self, status: int=0, message: str="", res_type: str="", keys: dict[str, str]={}, _data: str=""):
        if status: self.status = status
        if message: self.message = message
        if res_type: self.res_type = res_type
        
        if keys and _data:
            raise ResponseError("Keys and data cannot coexist in the same response.")

        self.keys = keys
        self._data = _data
    
    def stringify(self) -> str:
        string = ""

        string += f"{self.status}\r\n"

        content = ""
        if self.message:
            string += f"message:{self.message}\t\r\n"

        if self.res_type:
            string += f"type:{self.res_type}\t\r\n"

        if self.keys:
            for key in self.keys:
                content += f"{key}:{self.keys[key]}\t\r\n"

        if self._data:
            content = self._data
            

        if content:
            string += f"length:{len(content)}\t\r\n"
            string += f"hash:{hashlib.sha256(content.encode()).hexdigest()}\t\r\n"
            string += "\r\n\r\n"
            string += content
        else:
            string += "\r\n\r\n"

        return string

    def __str__(self):
        return self.stringify()
