import socket

from OpenSSL import SSL

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

        conn.send("Hello, world!\n".encode())
        conn.shutdown()
        conn.close()

if __name__ == "__main__":
    main()
