import socket

from OpenSSL import SSL

from lib.req import Request, RequestMethod, RequestParseError
from lib.res import Response

from lib.handle.get import handle_get_request
from lib.handle.put import handle_put_request

def main():
    ctx = SSL.Context(SSL.SSLv23_METHOD)
    ctx.use_privatekey_file("key.pem")
    ctx.use_certificate_file("cert.pem")

    server = SSL.Connection(ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 2693))
    server.listen(15)

    while True:
        conn, addr = server.accept()
        print(f"New connection from '{addr}'")

        try:
            handle_connection(conn, addr)
            print(f"Closing connection from '{addr}'")
        except RequestParseError as err:
            res = Response(err.code, "Malformed request")
            conn.send(res.stringify().encode())
            print(f"Closing connection from '{addr}' with error '{err}'")
        except Exception as err:
            res = Response(40, "Internal error")
            conn.send(res.stringify().encode())
            print(f"Closing connection from '{addr}' with error '{err}'")

        conn.shutdown()
        conn.sock_shutdown(socket.SHUT_RDWR)
        conn.close()



def handle_connection(conn, addr):
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
            res = handle_get_request(req)
        case RequestMethod.PUT:
            res = handle_put_request(req)

    conn.send(res.stringify().encode())



if __name__ == "__main__":
    main()
