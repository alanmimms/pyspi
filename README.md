# MicroPython SPI Programmer using ESP32 hardware

This is a project in progress. Its goal is to create a web page
driven, WIFI accessible, ESP32 based device that can be connected to a
SPI flash device and be used to read, verify, erase, and program the
device's contents using a simple browser-based user interface.

## Setting the WiFI configuration
For now, you have to define your WiFi credentials in the ESP32's
NonVolatileStorage (NVS) using something like the following via the
ESP32's serial console:

```
import esp32
config = esp32.NVS('config')
config.set_blob('essid', bytearray('your-wifi-essid'))
config.set_blob('password', bytearray('your-wifi-password'))
config.commit()
```

