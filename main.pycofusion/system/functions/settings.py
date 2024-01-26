from system.functions import oled_i2c
def readUsername():
    try:
        with open("/system/misc/settings.sys", "r") as file:
            username = file.readline().strip()
            return username
    except Exception as e:
        print("Error reading username:", e)
        oled_i2c.println('Username Error')
        oled_i2c.println(e)
        return None
    
    
def writeUser(username):
    try:
        with open("/system/misc/settings.sys", "r") as file:
            lines = file.readlines()
        with open("/system/misc/settings.sys", "w") as file:
            lines[0] = username + "\n"
            for line in lines:
                file.write(line)
    except Exception as e:
        print("Error writing username:", e)
        oled_i2c.println('Username Error')
        oled_i2c.println(e)       
        
def readVer():
    try:
        with open("/system/misc/settings.sys", "r") as file:
            version = file.readlines()[1].strip()
            return version
    except Exception as e:
        print("Error reading version:", e)
        oled_i2c.println('version Error')
        oled_i2c.println(e)
        return None
    

def readNWS():
    try:
        with open("/system/misc/settings.sys", "r") as file:
            boolean = file.readlines()[2].strip()
            return boolean
    except Exception as e:
        print("Error reading network startup properties:", e)
        oled_i2c.println("netstart fail")
        oled_i2c.println(e)
        return None
def writeNWS(boolean):
    try:
        with open("/system/misc/settings.sys", "r") as file:
            lines = file.readlines()
        with open("/system/misc/settings.sys", "w") as file:
            lines[2] = boolean + "\n"
            for line in lines:
                file.write(line)
    except Exception as e:
        print("Error writing network startup properties:", e)
        oled_i2c.println('netstart fail')
        oled_i2c.println(e)