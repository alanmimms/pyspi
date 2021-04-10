# MicroPython SPI Programmer using ESP32 hardware

This is a project in progress. Its goal is to create a web page
driven, WIFI accessible, ESP32 based device that can be connected to a
SPI flash device. The SPI flash device must implement the Common Flash
Interface (CFI) commands. The ESP32 can be used via the web UI to
read, verify, erase, and write the device's contents using a simple
browser-based user interface.

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



# Design
## Top level `index.html`

* Identifies the device attached via SPI pins.
  * Total size.
  * Erase size.
  * Write protect region(s)?

## Read page
`GET /read?addr=A&length=L`
* Read content of device to a file (downloads image).
  * Support Intel hex format.
  * Support binary format.
* Checksum of device content: Simple 8-bit sum, MD5, SHA1, SHA256, SHA384, SHA512.

## Write page
`POST /write?addr=A&length=L`
* `Content-Type: application/octet-stream` or `application/intel-hex`.
* Upload content in Intel hex or binary format.

## Erase page
`POST /erase?addr=A&length=L`
* Erase one or more or all erasable regions in the device.

## Verify page
`POST /verify?addr=A&length=L`
* `Content-Type: application/octet-stream` or `application/intel-hex`.
* Upload content in Intel hex or binary format and verify contents of device match precisely.
* Report on differences.

