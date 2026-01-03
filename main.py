from smbus2 import SMBus, i2c_msg
import time
from TMAG5273_defs import *

i2c_addr = TMAG5273_I2C_ADDRESS_INITIAL


class TMAG5273:
    def __init__(self, bus=1, address=TMAG5273_I2C_ADDRESS_INITIAL):
        """Empty constructor"""

    def begin(self):
        self.setMagneticChannel(TMAG5273_X_Y_Z_ENABLE)
        self.setTemperatureEn(True)
        self.setOperatingMode(TMAG5273_CONTINUOUS_MEASURE_MODE)
        self.setAngleEn(TMAG5273_NO_ANGLE_CALCULATION)
        self.setLowPower(TMAG5273_LOW_ACTIVE_CURRENT_MODE)
        self.setXYAxisRange(TMAG5273_RANGE_80MT)
        self.setZAxisRange(TMAG5273_RANGE_80MT)
        self.getError()
        if (self.getLowPower() != TMAG5273_LOW_ACTIVE_CURRENT_MODE or 
            (self.getOperatingMode() != TMAG5273_CONTINUOUS_MEASURE_MODE) or
            (self.getMagneticChannel() != TMAG5273_X_Y_Z_ENABLE) or 
            (self.getTemperatureEN() != TMAG5273_TEMPERATURE_ENABLE) or 
            (self.getAngleEn() != TMAG5273_NO_ANGLE_CALCULATION)):
            raise "Configuration is not as expected"

    @staticmethod
    def setBitFieldValue(bitfield, new_value, bit_mask, bit_lsb):
        """Macro
        - bitfield -: variable containing the bit field to set the value in
        - bit_mask -: mask for the bit field to set
        - bit_lsb -: least significant bit position of the bit field
        - new_value -: new value to set the bit field to
        Example Usage:
        angleReg = setBitFieldValue(angleReg, TMAG5273_ANGLE_CALCULATION_BITS, TMAG5273_ANGLE_CALCULATION_LSB, mydata);"""
        return (bitfield & ~bit_mask) | (new_value << bit_lsb)

    @staticmethod
    def getBitFieldValue(bitfield, bit_mask, bit_lsb):
        """Macro
        - bitfield -: variable containing the bit field to pull the value out
        - bit_mask -: mask for the bit field to pull out
        - bit_lsb -: least significant bit position of the bit field
        Example Usage:
        uint8_t mydata = getBitFieldValue(angleReg, TMAG5273_ANGLE_CALCULATION_BITS, TMAG5273_ANGLE_CALCULATION_LSB);"""
        return (bitfield & bit_mask) >> bit_lsb

    def setMagneticChannel(self, channel_mode):
        """@brief Sets the data acquisition from the following magnetic
        axis channels listed below
        @param channelMode Value that sets the channel for data acquisition
            0X0 = All magnetic channels off, DEFAULT
            0X1 = X Channel Enabled
            0X2 = Y Channel Enabled
            0X3 = X, Y Channel Enabled
            0X4 = Z Channel Enabled
            0X5 = Z, X Channel Enabled
            0X6 = Y, Z Channel Enabled
            0X7 = X, Y, Z Channel Enabled
            0X8 = XYX Channel Enabled
            0X9 = YXY Channel Enabled
            0XA = YZY Channel Enabled
            0XB = XZX Channel Enabled
            TMAG5273_REG_SENSOR_CONFIG_1 - bits 7-4"""
        
        if (channel_mode > TMAG5273_XZX_ENABLE):
            raise f"Invalid channel mode: {channel_mode}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_1)
            mode = TMAG5273.setBitFieldValue(mode, channel_mode, TMAG5273_CHANNEL_MODE_BITS, TMAG5273_CHANNEL_MODE_LSB)
            print(f"Setting magnetic channel config to: {hex(mode)}")
            bus.write_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_1, mode)


    def setTemperatureEn(self, temperatureEnable):
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_T_CONFIG)
            mode = TMAG5273.setBitFieldValue(mode, temperatureEnable, TMAG5273_TEMPERATURE_BITS, TMAG5273_TEMPERATURE_LSB)
            print(f"Setting temperature config to: {hex(mode)}")
            bus.write_byte_data(i2c_addr, TMAG5273_REG_T_CONFIG, mode)


    def setOperatingMode(self, opMode):
        """@brief Sets the operating mode from one of the 4 modes:
        stand-by mode, sleep mode, continuous measure mode, and
        wake-up and sleep mode.
        @param opMode value to set the operating mode of the device
            - 0X0 = Stand-by mode (starts new conversion at trigger event)
            - 0X1 = Sleep mode
            - 0X2 = Continuous measure mode
            - 0X3 = Wake-up and sleep mode (W&S Mode)
            TMAG5273_REG_DEVICE_CONFIG_2 - bit 1-0"""
        if (opMode > TMAG5273_WAKE_UP_AND_SLEEP_MODE):
            raise f"Invalid operating mode: {opMode}"

        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_DEVICE_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, opMode, TMAG5273_OPERATING_MODE_BITS, TMAG5273_OPERATING_MODE_LSB)
            bus.write_byte_data(i2c_addr, TMAG5273_REG_DEVICE_CONFIG_2, mode)
            match mode:
                case 0x0:
                    mode = "STANDBY_BY_MODE"
                case 0x1:
                    mode = "SLEEP_MODE"
                case 0x2:
                    mode = "CONTINUOUS_MEASURE_MODE"
                case 0x3:
                    mode = "WAKE_UP_AND_SLEEP_MODE"
                
            print(f"Operating mode set to: {mode}")
            


    def setAngleEn(self, angleEnable):
        if (angleEnable > TMAG5273_XZ_ANGLE_CALCULATION):
            raise f"Invalid angleEnable {hex(angleEnable)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, angleEnable, TMAG5273_ANGLE_CALCULATION_BITS, TMAG5273_ANGLE_CALCULATION_LSB)
            print(f"Setting angleEnable config to: {hex(mode)}")
            bus.write_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2, mode)


    def setLowPower(self, lpLnMode):
        """@brief Sets the device to low power or low noise mode
            @param lpLnMode Value to set the mode
            - 0X0 = Low active current mode
            - 0X1 = Low noise mode
            TMAG5273_REG_DEVICE_CONFIG_2 - bit 4"""
        if (lpLnMode > TMAG5273_LOW_NOISE_MODE):
            raise f"Invalid lpLnMode {hex(lpLnMode)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_DEVICE_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, lpLnMode, TMAG5273_LOW_POWER_BITS, TMAG5273_LOW_POWER_LSB)
            print(f"Setting low power mode config to: {hex(mode)}")
            bus.write_byte_data(i2c_addr, TMAG5273_REG_DEVICE_CONFIG_2, mode)


    def setXYAxisRange(self, xyAxisRange):
        if (xyAxisRange > TMAG5273_RANGE_80MT):
            raise f"Invalid xyAxisRange {hex(xyAxisRange)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, xyAxisRange, TMAG5273_XY_RANGE_BITS, TMAG5273_XY_RANGE_LSB)
            print(f"Setting xyAxisRange config to: {hex(mode)}")
            bus.write_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2, mode)


    def setZAxisRange(self, zAxisRange):
        if (zAxisRange > TMAG5273_RANGE_80MT):
            raise f"Invalid zAxisRange {hex(zAxisRange)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, zAxisRange, TMAG5273_Z_RANGE_BITS, TMAG5273_Z_RANGE_LSB)
            print(f"Setting zAxisRange config to: {hex(mode)}")
            bus.write_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2, mode)


    def getDeviceStatus(self):
        """@brief This function returns the device status register as its
        raw hex value. This value can be taken and compared to the main
        register as seen in the datasheet.
        The errors include an oscillator error, INT pin error detected,
        OTP CRC errors, or under voltage resistors.
            TMAG5273_REG_DEVICE_STATUS
        @return Device Status Register as a raw value."""
        deviceStatusReg = 0
        with SMBus(1) as bus:
            deviceStatusReg = bus.read_byte_data(i2c_addr, TMAG5273_REG_DEVICE_STATUS)
        return deviceStatusReg

    def getError(self):
        """Check the device status register to see if there is an issue"""
        statusReg = self.getDeviceStatus()
        if ((statusReg & (TMAG5273_DEVICE_STATUS_VCC_UV_ERROR_BITS | TMAG5273_DEVICE_STATUS_OTP_CRC_ERROR_BITS |
                        TMAG5273_DEVICE_STATUS_INT_ERROR_BITS | TMAG5273_OSCILLATOR_ERROR_BITS)) != 0):
            raise(f"Error detected. Status registry: {statusReg}")


    def getLowPower(self):
        lowPowerMode = 0
        with SMBus(1) as bus:
            lowPowerMode = bus.read_byte_data(i2c_addr, TMAG5273_REG_DEVICE_CONFIG_2)
        return TMAG5273.getBitFieldValue(lowPowerMode, TMAG5273_LOW_POWER_BITS, TMAG5273_LOW_POWER_LSB)


    def getOperatingMode(self):
        """
        @brief Returns the operating mode from one of the 4 listed below:
            0X0 = Stand-by mode (starts new conversion at trigger event)
            0X1 = Sleep mode
            0X2 = Continuous measure mode
            0X3 = Wake-up and sleep mode (W&S Mode)
            TMAG5273_REG_DEVICE_CONFIG_2 - bit 1-0
        @return Operating mode: stand-by, sleep, continuous, or wake-up and sleep
        """
        opMode = 0
        with SMBus(1) as bus:
            opMode = bus.read_byte_data(i2c_addr, TMAG5273_REG_DEVICE_CONFIG_2)
        return TMAG5273.getBitFieldValue(opMode, TMAG5273_OPERATING_MODE_BITS, TMAG5273_OPERATING_MODE_LSB)


    def getMagneticChannel(self):
        magChannel = 0
        with SMBus(1) as bus:
            magChannel = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_1)
        return TMAG5273.getBitFieldValue(magChannel, TMAG5273_CHANNEL_MODE_BITS, TMAG5273_CHANNEL_MODE_LSB)


    def getTemperatureEN(self):
        tempENreg = 0
        with SMBus(1) as bus:
            tempENreg = bus.read_byte_data(i2c_addr, TMAG5273_REG_T_CONFIG)
        return TMAG5273.getBitFieldValue(tempENreg, TMAG5273_TEMPERATURE_BITS, TMAG5273_TEMPERATURE_LSB)


    def getAngleEn(self):
        angleReg = 0
        with SMBus(1) as bus:
            angleReg = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2)
        return TMAG5273.getBitFieldValue(angleReg, TMAG5273_ANGLE_CALCULATION_BITS, TMAG5273_ANGLE_CALCULATION_LSB)
    

    def getXYAxisRange(self):
        xyRangeReg = 0
        with SMBus(1) as bus:
            xyRangeReg = bus.read_byte_data(i2c_addr, TMAG5273_REG_SENSOR_CONFIG_2)
        return TMAG5273.getBitFieldValue(xyRangeReg, TMAG5273_XY_RANGE_BITS, TMAG5273_XY_RANGE_LSB)
    

    def calculateMagneticField(self, rawData, range):
        """
        Simple function to calculate the Magnetic field strength in mT from raw sensor data
        Defining this in the class makes it 'inline' for efficiency
        
        To convert the raw magnetic data to mT, the datasheet equation (eq 10) is as follows:
        B = {-(D15*2^15 + D14*2^14 + ... + D1*2^1 + D0*2^0)/2^16 } * 2*|RANGE|
        
        Notes:
        
        - The first section is flipping the sign bit of the data value (2's complement format)
        This is just:  -1 * D
        
        B = { (-1 * D / 2^16 } * 2*|RANGE|
        = { (-1 * D / 2^16 } * 2*|RANGE|/1
        = ( (-1 * D * 2 * |RANGE| ) / 2^16
        = ( 2 * (-1 * D * |RANGE| ) ) / 2^16
        =  (-1 * D * |RANGE| ) ) / 2^15
        
        Note: 2^15 = 32768        
        """
        return (float)(-1 * range * rawData) / 32768


    def getXData(self):
        dataBuffer = []
        with SMBus(1) as bus:
            dataBuffer = bus.read_i2c_block_data(i2c_addr, TMAG5273_REG_X_MSB_RESULT, 2)
            xData = (dataBuffer[0] << 8) | dataBuffer[1]
            range = 40 if self.getXYAxisRange() == 0 else 80
            return self.calculateMagneticField(xData, range)
            # sfTkError_t readRegister(uint8_t *devReg, 
            #                           size_t regLength, 
            #                           uint8_t *data, 
            #                           size_t numBytes, 
            #                           size_t &readBytes, 
            #                           uint32_t read_delay = 0);
            # readRegister(TMAG5273_REG_X_MSB_RESULT, dataBuffer, 2, nRead)
            # read_block_data(i2c_addr, register) -> list
            # read_i2c_block_data(i2c_addr, register, length) -> list


print("Program started..")
sensor = TMAG5273()
try:
    sensor.begin()
    # while True:
    #     magX = sensor.getXData()
    #     print(f"magX: {magX}")
except KeyboardInterrupt:
    sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)