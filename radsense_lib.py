# Библиотека для работы с временем
import time

# Default radSens i2c device address
RS_DEFAULT_I2C_ADDRESS = 0x66

# Device id, default value: 0x7D
# Size: 8 bit
RS_DEVICE_ID_RG = 0x00

# Firmware version
# Size: 8 bit
RS_FIRMWARE_VER_RG = 0x01

# Radiation intensity (dynamic period T < 123 sec)
# Size: 24 bit
RS_RAD_INTENSY_DYNAMIC_RG = 0x03

# Radiation intensity (static period T = 500 sec)
# Size: 24 bit
RS_RAD_INTENSY_STATIC_RG = 0x06

# Contains the accumulated number of pulses registered by the module
# since the last I2C data reading. The value is reset each
# time it is read. Allows you to process directly the pulses
# from the Geiger counter and implement other algorithms. The value is updated
# when each pulse is registered.
# Size: 16 bit */
RS_PULSE_COUNTER_RG = 0x09

# This register is used to change the device address when multiple
# devices need to be connected to the same line at the same
# time. By default, it contains the value 0x66. At the end of recording, the new
# value is stored in the non-volatile memory of the microcontroller.
# Size: 8 bit
# Access: R/W*/
RS_DEVICE_ADDRESS_RG = 0x10

# Control register for a high-voltage voltage Converter. By
# default, it is in the enabled state. To enable the HV generator,
# write 1 to the register, and 0 to disable it. If you try to write other
# values, the command is ignored.
# Size: 8 bit
#Access: R/W*/
RS_HV_GENERATOR_RG = 0x11

# Contains the value coefficient used for calculating
# the radiation intensity. If necessary (for example, when installing a different
# type of counter), the necessary sensitivity value in
# imp/MKR is entered in the register. The default value is 105 imp/MKR. At the end of
# recording, the new value is stored in the non-volatile memory of the
# microcontroller.
# Size: 16 bit
# Access: R/W*/
RS_SENSITIVITY_RG = 0x12

# Control register for a indication diode. By
# default, it is in the enabled state. To enable the indication,
# write 1 to the register, and 0 to disable it. If you try to write other
# values, the command is ignored.
# Size: 8 bit
# Access: R/W*/
RS_LED_CONTROL_RG = 0x14

# Control register for a low power mode. to enable send 1 to the register, and 0 to disable)
# Size: 8 bit
# Access: R/W*/
RS_LMP_MODE_RG = 0x0C

class CG_RadSens_I2C:
    def __init__(self, i2c, addr=RS_DEFAULT_I2C_ADDRESS, external_vcc=False):
        self._new_cnt = 0
        self._pulse_cnt = 0
        self.i2c = i2c
        self.addr = addr
        self.updatePulses()
        res = bytearray(3)
        self.i2c.writeto(self.addr, bytes([RS_DEVICE_ID_RG]), False)
        self.i2c.readfrom_into(self.addr, res)
        self._chip_id = res[0]
        self._firmware_ver = res[1]


    # Get chip id, default value: 0x7D.
    def getChipId(self):
        return self._chip_id
    
    # Get firmware version.
    def getFirmwareVersion(self):
        return self._firmware_ver
    
    # Get radiation intensity (static period T = 500 sec).
    def getRadIntensyDynamic(self):
        self.updatePulses()
        self.i2c.writeto(self.addr, bytes([RS_RAD_INTENSY_DYNAMIC_RG]), False)
        res = bytearray(3)
        self.i2c.readfrom_into(self.addr, res)
        return ((res[0] << 16) | (res[1] << 8) | int(res[2])) / 10.0
    
    # Get radiation intensity (static period T = 500 sec).
    def getRadIntensyStatic(self):
        self.updatePulses()
        self.i2c.writeto(self.addr, bytes([RS_RAD_INTENSY_STATIC_RG]), False)
        res = bytearray(3)
        self.i2c.readfrom_into(self.addr, res)
        return ((res[0] << 16) | (res[1] << 8) | int(res[2])) / 10.0
    
    def updatePulses(self):
        self.i2c.writeto(self.addr, bytes([RS_PULSE_COUNTER_RG]), False)
        res = bytearray(2)
        self.i2c.readfrom_into(self.addr, res)
        self._new_cnt = (res[0] << 8) | res[1]
        self._pulse_cnt += self._new_cnt
            
    # Get the accumulated number of pulses registered by the module
    # since the last I2C data reading.
    def getNumberOfPulses(self):
        self.updatePulses()
        return self._pulse_cnt
    
    # Get current number of pulses
    def getNumberOfNewPulses(self):
        self.updatePulses()
        return self._new_cnt
    
    # Reset accumulated count
    def resetPulses(self):
        self._pulse_cnt = 0

    # Get sensor address.
    def getSensorAddress(self):
        self.i2c.writeto(self.addr, bytes([RS_DEVICE_ADDRESS_RG]), False)
        res = bytearray(1)
        self.i2c.readfrom_into(self.addr, res)
        _sensor_address = res[0]
        return _sensor_address
     
    # Get state of high-voltage voltage Converter.
    def getHVGeneratorState(self):
        self.i2c.writeto(self.addr, bytes([RS_HV_GENERATOR_RG]), False)
        res = bytearray(1)
        self.i2c.readfrom_into(self.addr, res)
        if res[0] == 1:
            return "on"
        return "off"
    
    # Get the value coefficient used for calculating the radiation intensity
    def getSensitivity(self):
        self.i2c.writeto(self.addr, bytes([RS_SENSITIVITY_RG]), False)
        res = bytearray(2)
        self.i2c.readfrom_into(self.addr, res)
        return res[1] * 256 + res[0]
    
    # Control register for a high-voltage voltage Converter. By
    # default, it is in the enabled state. To enable the HV generator,
    # write 1 to the register, and 0 to disable it. If you try to write other
    # values, the command is ignored.
    # @param state  true - generator on / false - generator off
    def setHVGeneratorState(self, value):
        self.i2c.writeto(self.addr, bytes([RS_HV_GENERATOR_RG, value]), False)
        time.sleep(0.015)
        self.i2c.writeto(self.addr, bytes([RS_HV_GENERATOR_RG]), False)
        res = bytearray(1)
        self.i2c.readfrom_into(self.addr, res)
        if res[0] == 1:
            return "set on"
        return "set off"
    
    # Control register for a low power mode. By
    # default, it is in the disabled? state. To enable the LP mode,
    # write 1 to the register, and 0 to disable it. If you try to write other
    # values, the command is ignored.
    # @param state  true - LP on / false - LP off
    def setLPmode(self, value):
        self.i2c.writeto(self.addr, bytes([RS_LMP_MODE_RG, value]), False)
        time.sleep(0.015)
        self.i2c.writeto(self.addr, bytes([RS_LMP_MODE_RG]), False)
        res = bytearray(1)
        self.i2c.readfrom_into(self.addr, res)
        if res[0] == 1:
            return "set on"
        return "set off"
    
    # Contains the value coefficient used for calculating
    # the radiation intensity. If necessary (for example, when installing a different
    # type of counter), the necessary sensitivity value in
    # Imp / uR is entered in the register. The default value is 105 Imp / uR. At the end of
    # recording, the new value is stored in the non-volatile memory of the
    # microcontroller.
    # @param sens sensitivity coefficient in Impulse / uR
    def setSensitivity(self, value):
        #self.i2c.writeto(self.addr, bytes([RS_SENSITIVITY_RG, value]), False)
        self.i2c.writeto(self.addr, bytes([RS_SENSITIVITY_RG, value & 0xFF]), False)
        time.sleep(0.015)
        self.i2c.writeto(self.addr, bytes([RS_SENSITIVITY_RG+0x01, value >> 8]), False)
        
        self.i2c.writeto(self.addr, bytes([RS_SENSITIVITY_RG]), False)
        res = bytearray(2)
        self.i2c.readfrom_into(self.addr, res)
        return "set " + str(res[1] * 256 + res[0])
    
    # Control register for a indication diode. By
    # default, it is in the enabled state. To enable the indication,
    # write 1 to the register, and 0 to disable it. If you try to write other
    # values, the command is ignored.
    # @param state  true - diode on / false - diode off
    def setLedState(self, value):
        self.i2c.writeto(self.addr, bytes([RS_LED_CONTROL_RG, value]), False)
        time.sleep(0.015)
        self.i2c.writeto(self.addr, bytes([RS_LED_CONTROL_RG]), False)
        res = bytearray(1)
        self.i2c.readfrom_into(self.addr, res)
        if res[0] == 1:
            return "set on"
        return "set off"
    
    # Get state of led indication.
    def getLedState(self):
        self.i2c.writeto(self.addr, bytes([RS_LED_CONTROL_RG]), False)
        res = bytearray(1)
        self.i2c.readfrom_into(self.addr, res)
        if res[0] == 1:
            return "on"
        return "off"