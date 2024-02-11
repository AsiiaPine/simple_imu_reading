The repository comtains everything for IMU data reading via micropython firmware for [ESP32](https://micropython.org/download/ESP32_GENERIC/)

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Install python packages ](#install-python-packages-)
- [ESP32 part  :](#esp32-part--)
  - [Flash the firmware ](#flash-the-firmware-)
    - [Micropython Installation instructions ](#micropython-installation-instructions-)
    - [Program uploading instruction ](#program-uploading-instruction-)
  - [Read messages from USB device:](#read-messages-from-usb-device)
  - [Code](#code)


# Install python packages <a name="install_env"></a>
Create python environment with all dependencies:

```
python -m venv_name /path_to_new_virtual_environment
source /path_to_new_virtual_environment/venv_name/bin/activate  
pip install -r requirements.txt
```

# ESP32 part  <a name="esp_part"></a>:
All the code is stored in [esp32_part](esp32_part) 
Remember that the program entry point is [main.py](esp32_part/main.py)

## Flash the firmware <a name="esp_flash"></a>
### Micropython Installation instructions <a name="micropython_flash"></a>
Program your board using the esptool program, found [here](https://micropython.org/download/ESP32_GENERIC/).

If you are putting MicroPython on your board for the first time then you should first erase the entire flash using:

```
esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
```
<!-- From then on program the firmware starting at address 0x1000: -->
### Program uploading instruction <a name="esp_upload"></a>
Load the program via the instruction:
```
ampy --port /dev/ttyUSB0 put esp32_part/
```


## Read messages from USB device:

Install picocom
```
sudo apt-get install picocom
```
Check the port connected to the device:

```
ld /dev/ttyUSB*
```
Use the port name when start reading data via picocom. Use default baudrate with *-b* flag
```
 sudo picocom /dev/ttyUSBn -b 115200
```

## Code 

example with sensor calibration:



