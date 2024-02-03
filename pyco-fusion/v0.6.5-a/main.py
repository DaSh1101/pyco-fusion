print('loading PycoFusion')
from system.functions import wifi
from system.functions import sysInfo
from system.functions import file_manager
from system.functions import networking
from system.functions import serve
from system.functions import settings
from system.functions import oled_i2c
from machine import Pin

import socket
import machine
import os
import uos
import re
import utime
import time
import machine
import time
rootUser = settings.readUsername()
systemVersion = settings.readVer()

currentProcessName = "PycoFusion"
runningProcess = False

if not wifi.check_wifi_connection():
    if not settings.readNWS() == 'false':
        wifi.wlanConnectToSavedNetworks()

if not rootUser:  # login stage
    rootUser = input("PycoFusion " + systemVersion + " finished loading, login: ")
    settings.writeUser(rootUser)
    print(r'User: ', rootUser, ' logged in')
else:
    print("PycoFusion", systemVersion, "finished loading, logged in as:", rootUser)

oled_i2c.println("PycoFusion")
oled_i2c.println(systemVersion)

while True: #main OS
    oled_i2c.println(os.getcwd() + "$ ")
    command = input(rootUser + r"@pico:" + os.getcwd() + "~$ " "")  # save command as 'command'
    oled_i2c.printOled(command)

    if command == 'wlan connect':
        wifi.wlanConnect()


    elif command.startswith("download"):
       parts = command.split()
       if len(parts) == 3 and parts[0] == "download":
           _, url, filename = parts
           networking.dload(url, filename)
       else:
            print("Invalid download command. Please use the format 'download <url> <filename>'.")
            oled_i2c.println('Invalid Format')

    elif command.lower().startswith("delete") or command.lower().startswith("del"):
        parts = command.split(" ", 1)
        if len(parts) == 2:
            file_to_delete = parts[1]
            file_manager.delete(file_to_delete)
        else:
            print("Invalid delete command format. Use 'delete file_name' or 'del file_name'.")
            oled_i2c.println('Invalid Format')
        
    elif command == "wlan disconnect":
        wifi.wlanDisconnect()


    elif command == "wlan scan":
        wifi.wlanScan()


    elif command == "wlan info" or command == "wlan status":
        wifi.wlanActive()


    elif command == "wlan":
        print('wlan + {connect, disconnect, scan, info}')
        oled_i2c.println('Check Docs')

    elif command == "temp":
        sysInfo.temp()


    elif command == "system":
        print("system commands 'temp'")
        oled_i2c.println('Check Docs')

    elif command == 'ls' or command == 'dir':
        file_manager.oslistdir()


    elif command.startswith('write'):
        parts = command.split()
        if len(parts) > 1:
            file_to_write = ' '.join(parts[1:])
            file_manager.createFile(file_to_write)
        else:
            print("Invalid write command format. Use 'write file_name'.")
            oled_i2c.println('Invalid Format')
    elif command.startswith('mkdir'):
        parts = command.split()
        if len(parts) > 1:
            directory_path  = ' '.join(parts[1:])
            file_manager.mkdir(directory_path)
            
        else:
            print("Invalid write command format. Use 'mkdir path'.")
            oled_i2c.println('Invalid Format')
        
    elif command.startswith('rmdir'):
        parts = command.split()
        if len(parts) > 1:
            directory_path  = ' '.join(parts[1:])
            file_manager.rmdir(directory_path)
            
        else:
            print("Invalid write command format. Use 'rmdir path'.")
        
    elif command.startswith('print') or command.startswith('echo'):
        parts = command.split()
        if len(parts) > 1:
            echoTXT = ' '.join(parts[1:])
            print(echoTXT)
            oled_i2c.println(echoTXT)
        
        
    elif command.startswith('edit'):
        try:
            file = command.split()[1]
        except Exception as e:
            file = ""
        open(file)
        file_manager.editFile(file)


    elif command == 'fman':
        print('[write] creates a new file')
        print('[open] reads a file and runs python files')
        print('[edit] edits a file')
        oled_i2c.println('Check Docs')
        
    elif command == "cd..":
        os.chdir("..")
    elif command.startswith("relog"):
        parts = command.split()
        if len(parts) > 1:
            rootUser = ' '.join(parts[1:])
            settings.writeUser(rootUser)
            print("User:", rootUser.strip(), "logged in")
        else:
            print("Invalid relog command format. Use 'relog root_user'.")
            oled_i2c.println('Invalid Format')

    elif command.startswith("open") or command.startswith("read") or command.startswith("view"):
        currentProcessName = filename
        parts = command.split()
        if len(parts) > 1:
            filename = " ".join(parts[1:])
            try:
                os.stat(filename)
                if filename.endswith(".py"):
                    runningProcess = True
                    
                    try:
                        subprocess.Popen(["python", filename])
                        print(f'Opened subprocess: {filename}')
                        oled_i2c.println(f'Opening {filename}')
                    except KeyboardInterrupt:
                        print(f'Closing subprocess: {filename}')
                        oled_i2c.println(f'Closing {filename}')
                        runningProcess = False
                else:
                    with open(filename, 'r') as f:
                        content = f.read()
                        print(content)
                    print(f"Opened {filename} successfully.")
                    oled_i2c.println(f'Opened {filename}')
            except OSError:
                print(f"File {filename} does not exist.")
                oled_i2c.println('Invalid File')
        else:
            print("Invalid command. Please use the format: open filename")
            oled_i2c.println('Invalid Format')
        

    elif command.startswith("move "):
        parts = command.split()
        if len(parts) == 3:
            _, file_to_move, destination_path = parts
            file_manager.move_file(file_to_move, destination_path)
        else:
            print("Invalid move command. Please use the format 'move filename destination'.")
            oled_i2c.println('Invalid Format')
            
    elif command == 'serve':
        serve.serve()
        
        
    elif command == 'help':
        print('System Version: ' + systemVersion)
        print('Example: move /file.txt /destination/file.txt')
        print('\nAvailable Commands:')
        print('[operations] [arguments]')
        print('dir or ls:           Lists files in the current directory')
        print('delete or del:       Deletes a file')
        print('download [filename]: Downloads a file. Example: download https://example.com ex.html')
        print('edit                 [filename]: Edits the selected file')
        print('exit:                Exits to Python mode. To come back, type "import main"')
        print('help:                Displays this help message')
        print('move                 [source | destination]: Moves the selected file')
        print('relog                [username]: Allows the user to change the username. Example: "relog dash"')
        print('serve:               Serves specified files as a webpage')
        print('wlan                 [connect] [disconnect] [status] [scan] [runonstart] [autoconnect]: Configures WiFi variables')
        print('write                [filename]: Writes a file')
        oled_i2c.println('Check Docs...')
        

        
    elif command == 'wlan runonstart':
        current_state = settings.readNWS()
        new_state = 'false' if current_state == 'true' else 'true'
        print('Wi-Fi Run on Start:', new_state)
        oled_i2c.println('AutoWiFi: ' + new_state)
        settings.writeNWS(new_state)

            
    elif command == 'exit':
        print('Leaving PycoFusion')
        oled_i2c.println('Now Exiting:')
        oled_i2c.println('PycoFusion0.6.5a')
        break
    elif command.startswith('chdir') or command.startswith('cd'):
        directory = command.split()[1]
        os.chdir(directory)
    else:
        try:
            filename = command # join the parts of the command after the first one into a single string
            try: # try to get the file information
                os.stat(filename)
                if filename.endswith(".py"): # check if the file is a .py file
                    execfile(filename)
                else:
                    f = open(filename, 'r') # open the file in read mode
                    content = f.read() # read the file content as a string
                    f.close() # close the file
                    print(content)
            except OSError: # handle the case when the file does not exist
                print(f"E: {filename} is not a valid function, or operable file.")
                oled_i2c.println(f"E: {filename} isn't a valid function")
        except Exception as e:
        
            print("An exception occurred:", e)