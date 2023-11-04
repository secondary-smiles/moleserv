import socket

from OpenSSL import SSL

from lib.req import Request

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
            conn.shutdown()
            print(f"Closing connection from '{addr}'")
        except Exception as err:
            print(f"Closing connection from '{addr}' with error '{err}'")

        conn.close()


def handle_connection(conn, addr):
    while True:
        read_bytes = ""
        try:
            read_bytes = conn.recv(2048).decode()
        except SSL.ZeroReturnError:
            break

        sections = read_bytes.split("\r\n\r\n")
        if len(sections) < 2:
            raise Exception("No headers, or headers too long.")

        headers = sections[0]
        req = Request(headers)
        print(req)


if __name__ == "__main__":
    main()
