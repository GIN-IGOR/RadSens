# Библиотека для работы с временем
import time
# Библиотека для работы с пинами ввода-вывода
from machine import Pin, I2C
# Библиотека для работы со светодиодами WS2812
from ssd1306_lib import SSD1306_I2C
# Библиотека для работы с модулем RadSens
from radsense_lib import CG_RadSens_I2C

# Номер пина, к которому подключен SCL I2C
scl_pin = 9
# Номер пина, к которому подключен SDA I2C
sda_pin = 8

# I2C
# Указываем пин I2C
i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)

# Указываем параметры OLED
oled_width = 128
oled_height = 32
oled = SSD1306_I2C(oled_width, oled_height, i2c)
# Указываем параметры radsense
radsense = CG_RadSens_I2C(i2c)

oled.fill(0)
print("ChipId: ", hex(radsense.getChipId()))
oled.text("ChipId: " + str(hex(radsense.getChipId())), 0, 0, 1)
print("Firmware: ", radsense.getFirmwareVersion())
oled.text("Firmware: " + str(radsense.getFirmwareVersion()), 0, 15, 1)
oled.show()
time.sleep(2)
oled.fill(0)
print("Sensitivity: ", radsense.getSensitivity())
oled.text("Sens-ty: " + str(radsense.getSensitivity()), 0, 0, 1)
print("LED state: ", radsense.getLedState())
oled.text("LED state: " + str(radsense.getLedState()), 0, 15, 1)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()

while True:
    print("Dyn: ", radsense.getRadIntensyDynamic())
    print("Sta: ", radsense.getRadIntensyStatic())
    print("Pul: ", radsense.getNumberOfPulses())
    oled.fill(0)
    oled.text("Dyn: " + str(radsense.getRadIntensyDynamic()), 0, 0, 1)
    oled.text("Sta: " + str(radsense.getRadIntensyStatic()), 0, 15, 1)
    oled.show() 
    time.sleep(10)
    
    
