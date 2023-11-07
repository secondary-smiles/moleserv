import os
import socket

from OpenSSL import SSL
from typing import Callable

from moleserv.response import Response
from moleserv.request import Request, RequestMethod, RequestParseError

class PathNotFoundError(Exception):
    pass

class Server:
    keyfile: str
    certfile: str

    address: str
    port: int

    _get_paths: dict[str, Callable[[Request], Response]] = {}
    _put_paths: dict[str, Callable[[Request], Response]] = {}
    _del_paths: dict[str, Callable[[Request], Response]] = {}

    def __init__(self, address: str, port: int=2693):
        self.address = address
        self.port = port
    
    def get(self, path: str, callback: Callable[[Request], Response]):
        self._get_paths[path] = callback
        return self

    def put(self, path: str, callback: Callable[[Request], Response]):
        self._put_paths[path] = callback
        return self

    def delete(self, path: str, callback: Callable[[Request], Response]):
        self._del_paths[path] = callback
        return self

    def listen(self, keyfile: str, certfile: str):
        self.keyfile = keyfile
        self.certfile = certfile

        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file(self.keyfile)
        ctx.use_certificate_file(self.certfile)

        server = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 2693))
        server.listen(15)

        while True:
            conn, addr = server.accept()
            print(f"New connection from '{addr}'")

            try:
                self._handle_connection(conn)
                print(f"Closing connection from '{addr}'")
            except RequestParseError as err:
                res = Response(err.code, "Malformed request")
                conn.send(res.stringify().encode())
                print(f"Closing connection from '{addr}' with error '{err}' and code '{err.code}'")
            except PathNotFoundError as err:
                res = Response(32, "Not found")
                conn.send(res.stringify().encode())
                print(f"Closing connection from '{addr}' with error '{err}' and code '32'")
            except Exception as err:
                res = Response(40, "Internal error")
                conn.send(res.stringify().encode())
                print(f"Closing connection from '{addr}' with error '{err}' and code '40'")

            conn.shutdown()
            conn.sock_shutdown(socket.SHUT_RDWR)
            conn.close()

    def _handle_connection(self, conn):
        total_data = ""
        total_bytes_read = 0

        data = conn.recv(2048).decode()
        total_data += data
        total_bytes_read += len(data)

        sections = data.split("\r\n\r\n")
        if len(sections) < 2:
            raise Exception("No headers, or headers too long")

        req = Request(data)


        while total_bytes_read < req.length:
            data = conn.recv(total_bytes_read).decode()
            total_data += data
            total_bytes_read += len(data)

            req = Request(total_data)


        res = Response()
        match req.kind:
            case RequestMethod.GET:
                if req.url.path in self._get_paths:
                    res = self._get_paths[req.url.path](req)
                else:
                    raise PathNotFoundError(f"Path '{req.url.path}' not found")
            case RequestMethod.PUT:
                if req.url.path in self._put_paths:
                    res = self._put_paths[req.url.path](req)
                else:
                    raise PathNotFoundError(f"Path '{req.url.path}' not found")
            case RequestMethod.DEL:
                if req.url.path in self._del_paths:
                    res = self._del_paths[req.url.path](req)
                else:
                    raise PathNotFoundError(f"Path '{req.url.path}' not found")

        conn.send(res.stringify().encode())
