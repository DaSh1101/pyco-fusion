from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# List to store lines of text
lines = [""] * 6  # Adjust the number of lines based on your display size

def update_display():
    oled.fill(0)  # Clear the display
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 10)  # Adjust the vertical spacing as needed
    oled.show()

def printOled(text):
    # Split the text into chunks that fit on the display
    max_chars = 16  # Adjust this value based on your display size
    s = str(text)
    chunks = [s[i:i+max_chars] for i in range(0, len(s), max_chars)]
    
    # Append new text to the last line
    lines[-1] += chunks[0]

    # If there are additional chunks, add them as new lines
    if len(chunks) > 1:
        lines.extend(chunks[1:])

    update_display()

def println(text):
    # Split the text into chunks that fit on the display
    max_chars = 16  # Adjust this value based on your display size
    s = str(text)
    chunks = [s[i:i+max_chars] for i in range(0, len(s), max_chars)]
    
    for chunk in chunks:
        lines.pop(0)  # Remove the first line
        lines.append(chunk)  # Add new text at the end
        update_display()

# Initial display
update_display()
