# PycoFusion

## Version: 0.6.5a

PycoFusion is a lightweight open-source operating system written in MicroPython for the Raspberry Pi Pico W. It provides a platform for running user-written Python code, along with several built-in features to enhance functionality.

## Installation

Installing PycoFusion is a straightforward process. Follow these steps:

1. Open your preferred IDE (Integrated Development Environment).
2. Download the latest release of PycoFusion (`pyco[ver].zip`) from the [Releases](https://github.com/DaSh1101/pyco-fusion/releases) page.
3. Extract the downloaded ZIP file to your local machine.
4. Connect your Raspberry Pi Pico W to your computer.
5. Drag and drop the extracted files to the root directory of your Raspberry Pi Pico W.
6. Save the changes and run `main.py` to start PycoFusion.

## Features

### 1. User-Written Python Code
- Execute custom Python code on your Raspberry Pi Pico W using PycoFusion.

### 2. Built-in File Manager
- Modify files and directories effortlessly.
- Rename and move files with ease.

### 3. Networking Capabilities
- Pre-loaded networking capabilities for seamless connectivity.
- Download files directly from the internet.
- Host local files and public sites (requires port forwarding).
- Toggle to scan through a list of saved networks and auto-connect.

### 4. OLED I2C Display Support
- Custom-made drivers to support ssd1306 OLED I2C displays.
- [WARNING] These will no longer be supported in future versions, in favor of HDMI or LCD displays
- You can modify the code to hearts desire though if you'd like to add support!
## Getting Started

To get started with PycoFusion, follow the installation steps mentioned above. Once installed, explore the built-in features and customize your experience.

## Usage

#### Running Python Code
```python
user@pico:/~$ write test.py
type {#done#} and hit return to save
print("Hello Fusion!")
{#done#}
Creating/Overwriting file...
user@pico:/~$ test.py
Hello Fusion!
user@pico:/~$
```

### File Management
Use the built-in file manager to navigate, modify, and organize your files.

`write "Filename"` Creates a new file with the given name, then allows you to write files contents
`mkdir "Directory Name"` Creates a new directory with the given name
`dir` Lists files in a given directory
`ls` Lists files in a given directory
`cd "Directory"` Changes current working directory
`chdir "Directory"` changes current working directory
`edit "filename"` Reads a file, then opens it to make changes / overwrite

### Networking
Configure networking settings and take advantage of the pre-loaded capabilities.

`download url://url.url "filename"` Attempts to download file from given url

### OLED I2C Display
Custom-made display drivers to take advantage of your display.
`Currently only supports: ssd1306 oled i2c displays`

### Contributing
If you'd like to contribute to the development of PycoFusion, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and submit a pull request.

### License
PycoFusion is licensed under the MIT License.

### Release Notes
**Version 0.6.5a**
- Initial VERY EARLY release of PycoFusion.
- Added support for running user-written Python code.
- Introduced a built-in file manager.
- Integrated networking capabilities.
- Added support for [OLED I2C](https://www.amazon.com/dp/B06XRBTBTB/) displays.
