import hashlib

class ResponseError(Exception):
    pass

class Response:
    status: int = 10
    message: str = ""
    content_type: str = ""
    len: int
    hash: str

    keys: dict[str, str]
    content: str

    def __init__(self, status: int=0, message: str="", content_type: str="text/molerat", keys: dict[str, str]={}, content: str=""):
        if status: self.status = status
        if message: self.message = message
        if content_type: self.content_type = content_type
        
        if keys and content:
            raise ResponseError("Keys and data cannot coexist in the same response")

        self.keys = keys
        self.content = content
    
    def stringify(self) -> str:
        string = ""

        string += f"{self.status}\r\n"

        content = ""
        if self.message:
            string += f"message:{self.message}\t\r\n"

        if self.keys:
            for key in self.keys:
                content += f"{key}:{self.keys[key]}\t\r\n"

        if self.content:
            content = self.content
            

        if content:
            if self.content_type:
                string += f"type:{self.content_type}\t\r\n"
            else:
                raise ResponseError("Content defined without content_type")

            string += f"length:{len(content)}\t\r\n"
            string += f"hash:{hashlib.sha256(content.encode()).hexdigest()}"
            string += "\r\n\r\n"
            string += content
        else:
            string += "\r\n\r\n"

        return string

    def __str__(self):
        return self.stringify()
