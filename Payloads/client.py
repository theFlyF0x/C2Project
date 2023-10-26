import socket

HOST = "127.0.0.1" # C2 Server IP
PORT = 6969 # C2 application port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT)) # Connect to the C2 server
    sock.sendall(b"ciao")