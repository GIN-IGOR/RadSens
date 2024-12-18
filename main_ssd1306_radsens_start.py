# Библиотека для работы с временем
import time
# Библиотека для работы с пинами ввода-вывода
from machine import Pin, I2C
# Библиотека для работы с модулем дисплея ssd1306
from ssd1306_lib import SSD1306_I2C
# Библиотека для работы с модулем RadSens
from radsense_lib import CG_RadSens_I2C

# Номер пина, к которому подключен SCL I2C
scl_pin = 9
# Номер пина, к которому подключен SDA I2C
sda_pin = 8

# I2C
# Объявление шины I2C
i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)

# Параметры модуля дисплея OLED
oled_width = 128
oled_height = 32
# Объявление модуля дисплея OLED
oled = SSD1306_I2C(oled_width, oled_height, i2c)
# Объявление модуля RadSens
radsense = CG_RadSens_I2C(i2c)

# Очистка содержимого на модуле дисплея
oled.fill(0)
# Вывод технической информации в порт
print("ChipId: ", hex(radsense.getChipId()))
print("Firmware: ", radsense.getFirmwareVersion())
# Формирование информации для отображения на модуле дисплея
oled.text("ChipId: " + str(hex(radsense.getChipId())), 0, 0, 1)
oled.text("Firmware: " + str(radsense.getFirmwareVersion()), 0, 15, 1)
# Показ содержимого на модуле дисплея
oled.show()

# Пауза 2 секунды
time.sleep(2)

# Очистка содержимого на модуле дисплея
oled.fill(0)
# Вывод технической информации в порт
print("Sensitivity: ", radsense.getSensitivity())
print("LED state: ", radsense.getLedState())
# Формирование информации для отображения на модуле дисплея
oled.text("Sens-ty: " + str(radsense.getSensitivity()), 0, 0, 1)
oled.text("LED state: " + str(radsense.getLedState()), 0, 15, 1)
# Показ содержимого на модуле дисплея
oled.show()

# Пауза 2 секунды
time.sleep(2)

# Очистка содержимого на модуле дисплея
oled.fill(0)
# Показ содержимого на модуле дисплея
oled.show()

while True:
    # Вывод информации в порт
    print("Dyn: ", radsense.getRadIntensyDynamic())
    print("Sta: ", radsense.getRadIntensyStatic())
    print("Pul: ", radsense.getNumberOfPulses())
    # Очистка содержимого на модуле дисплея
    oled.fill(0)
    # Формирование информации для отображения на модуле дисплея
    oled.text("Dyn: " + str(radsense.getRadIntensyDynamic()), 0, 0, 1)
    oled.text("Sta: " + str(radsense.getRadIntensyStatic()), 0, 15, 1)
    # Показ содержимого на модуле дисплея
    oled.show()
    # Пауза 10 секунд
    time.sleep(10)
