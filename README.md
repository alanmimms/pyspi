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
## ReST API structure 

## Top level `index.html`

* Identifies the device attached via SPI pins.
  * Total size.
  * Erase size.
  * Write protect region(s)?

## ReST API
* URIs for read, write, erase, verify
* URI segment parameters:
  * `address` - address to start operation in ASCII hex
  * `length` - length of operation in ASCII hex
* For read, write, verify: `Content-Type: application/octet-stream` or `application/intel-hex`.

### Read page
`GET /read/`_address_`/`_length_
* Read content of device to a file (downloads image).
  * Support Intel hex format.
  * Support binary format.
* Checksum of device content: Simple 8-bit sum, MD5, SHA1, SHA256, SHA384, SHA512.
* Special case for length of `*` to indicate entire device content.

### Write page
`POST /write/`_address_`/`_length_
* Upload content in Intel hex or binary format.

### Erase page
`POST /erase/`_address_`/`_length_
* Erase part of all of the device.
* Special case for length of `*` to indicate entire device content.

### Verify page
`POST /verify/`_address_`/`_length_
* Upload content in Intel hex or binary format and verify contents of device match precisely.
  * Only compares number of bytes uploaded as image.
* Report on differences.
