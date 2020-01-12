# W600_Smart_Plug
 Code to allow the LSPA7 to be controlled via MQTT using MicroPython
 
 The LSPA7 is one of the model numbers used for the Tuya smart plug that used to be powered by the ESP8266 but now uses the Winner Micro W600.
 
# Flashing MicroPython
 MicroPython is flashed with the wm_600.fls file from [Winner Micro' website](http://www.winnermicro.com/en/html/1/156/158/497.html) using the [W600 tool](https://github.com/wemos/w600tool)
 The RX Pin of the W600 is also used for the push button on the side. The pull up resistor for the button is 1kΩ, which makes it hard for a USB-Serial Converter to pull the pin low. This makes it hard to reprogram the W600. A buffer amplifier can be used to allow the USB-Serial Converter to program the W600.
