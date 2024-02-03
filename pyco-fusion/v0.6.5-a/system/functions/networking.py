import requests
from system.functions import oled_i2c

def dload(url, filename):
    
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        file.close()
        print(f"Downloaded {filename} successfully.")
        oled_i2c.println("Download Done.")
        oled_i2c.println(f"{filename}")
        
    else:
        print(f"Download failed with status code {response.status_code}.")
        oled_i2c.println("Download Failed")
        oled_i2c.println(f"{response.status_code}")