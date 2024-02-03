import os
import uos
from system.functions import oled_i2c

def oslistdir():
    files = os.listdir() # get the list of files
    oled_i2c.println(", ".join(files)) 
    print("\n".join(files)) # print the list with new lines
def move_file(source, destination):
    try:
        # Check if the source file exists
        if not source in uos.listdir():
            print(f"Error: The file '{source}' does not exist.")
            oled_i2c.println(f"{source} doesn't exist")
            return

        # Check if the source is a directory
        source_is_directory = False
        try:
            source_is_directory = uos.stat(source)[0] & 0o170000 == 0o040000
        except:
            pass

        if source_is_directory:
            print(f"Error: '{source}' is a directory. Use a file for the move operation.")
            oled_i2c.println(f"{source} is a dir")
            return

        # Remove trailing slash from destination if present
        destination = destination.rstrip('/')

        # Move the file to the destination
        uos.rename(source, destination)
        print(f"File '{source}' moved to '{destination}' successfully.")
        oled_i2c.println(f"{source} -> {destination}")
    except Exception as e:
        print(f"An exception occurred: {e}")
        oled_i2c.println(f"err: {e}")


def createFile(file):
    if len(file) == 0:
        filename = input('Choose a name for your file: ')
        oled_i2c.println("Choose name")
    else:
        filename = file
    input_lines = []
    print('type {#done#} and hit return to save')
    oled_i2c.println("type {#done#}")
    while True:
        line = input()
        if line == "{#done#}":
            break
        input_lines.append(line)
    text = "\n".join(input_lines)
    print('Creating/Overwriting file...')
    oled_i2c.println("Writing...")
    with open(filename, "w") as file:
        file.write(text)

def mkdir(directory_path):
    try:
        # Check if the directory already exists
        if not directory_path in uos.listdir():
            # Create the directory
            uos.mkdir(directory_path)
            print(f"Directory '{directory_path}' created successfully.")
            oled_i2c.println(f"{directory_path} success")
        else:
            print(f"Directory '{directory_path}' already exists.")
            oled_i2c.println(f"{directory_path} exists")
    except Exception as e:
        print(f"Error creating directory: {e}")
        oled_i2c.println("err creating dir")
        oled_i2c.println(f"{e}")

def rmdir(directory_path):
    try:
        # Check if the directory exists
        if directory_path in uos.listdir():
            # Remove the directory
            uos.rmdir(directory_path)
            print(f"Directory '{directory_path}' removed successfully.")
            oled_i2c.println(f"{directory_path} deleted")
        else:
            print(f"Directory '{directory_path}' does not exist.")
            oled_i2c.println(f"{directory_path} doesn't exist")
    except Exception as e:
        print(f"Error removing directory: {e}")
        oled_i2c.println(f"err removing dir")
def editFile(file):
    if len(file) == 0:
        filename = input("Type the name of the file you'd like to edit: ")
        oled_i2c.println("Type filename")
        file = open(filename, "w")  # Open the file in write mode
    else:
        file = open(file, "w")  # Open the file in write mode

    print('type {#done#} and hit return to save')
    oled_i2c.println("Type {#done#}")
    input_lines = []
    while True:
        line = input("")
        if line == "{#done#}":
            break
        input_lines.append(line)

    new_content = "\n".join(input_lines)
    file.write(new_content)
    
    file.close()

def delete(file):
    try:
        os.remove(file)
        print(f"File '{file}' deleted successfully.")
        oled_i2c.println(f"{file} deleted")
    except OSError as e:
        print(f"Error deleting file '{file}': {e}")
        oled_i2c.println(f"err deleting {file}: {e}")
    
