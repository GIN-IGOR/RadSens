"radsense_lib.py" - this library is an adaptation (ported version) for micropython of the official library: https://github.com/climateguard/RadSens
"main_ssd1306_radsens_start.py" - this is an example of using the library "radsense_lib.py"

The code is tested on ESP32-C3. The total consumption of the "radsense ver 4.0" module + "ESP32-C3" microcontroller + "ssd1306" 0.91" oled screen is about 20 milliamps at 3.3 volts. The modules are on the same i2c bus.
Be sure to remove the i2c bus pull-up resistors (2 pieces of 4.7 kOhm) on the "radsense ver 4.0" module board or on the "ssd1306" 0.91" oled screen board) otherwise there will be an i2c error.
