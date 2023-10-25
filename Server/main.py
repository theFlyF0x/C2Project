import socket

HOST = "127.0.0.1"
PORT = "6969"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()
    with conn: 
        print(f"Connesso a {addr}")
        data = conn.recv(1024)
        print(data)