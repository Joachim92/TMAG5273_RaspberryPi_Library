from smbus2 import SMBus
from TMAG5273_RaspberryPi_Library_Defs import *

def printOperatingMode(mode):
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


class TMAG5273:
    def __init__(self):
        """Empty Constructor"""

    def begin(self):
        """
        @brief Begin communication with the TMAG over I2C, initialize it, and
        and set the wire for the I2C communication
        @param sensorAddress I2C address of the sensor
        @param wirePort I2C port to use for communication, defaults to Wire
        @return Error code (1 is success, 0 is failure, negative is warning)        
        """
        self.setMagneticChannel(TMAG5273_X_Y_Z_ENABLE)
        self.setTemperatureEn(True)
        self.setOperatingMode(TMAG5273_CONTINUOUS_MEASURE_MODE)
        self.setAngleEn(TMAG5273_NO_ANGLE_CALCULATION)
        self.setLowPower(TMAG5273_LOW_ACTIVE_CURRENT_MODE)
        self.setXYAxisRange(TMAG5273_RANGE_40MT)
        self.setZAxisRange(TMAG5273_RANGE_40MT)
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
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_1)
            mode = TMAG5273.setBitFieldValue(mode, channel_mode, TMAG5273_CHANNEL_MODE_BITS, TMAG5273_CHANNEL_MODE_LSB)
            print(f"Setting magnetic channel config to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_1, mode)


    def setTemperatureEn(self, temperatureEnable):
        """
        @brief Sets the enable bit that determines the data acquisition of the
         temperature channel.
        @param temperatureEnable Value to determine enable or disable
            0x0 = Temp Channel Disabled
            0x1 = Temp Channel Enabled
            TMAG5273_REG_T_CONFIG - bit 0
        @return Error code (0 is success, negative is failure, positive is warning)
        """
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_T_CONFIG)
            mode = TMAG5273.setBitFieldValue(mode, temperatureEnable, TMAG5273_TEMPERATURE_BITS, TMAG5273_TEMPERATURE_LSB)
            print(f"Setting temperature config to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_T_CONFIG, mode)


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
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, opMode, TMAG5273_OPERATING_MODE_BITS, TMAG5273_OPERATING_MODE_LSB)
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_2, mode)
        printOperatingMode(mode)


    def setAngleEn(self, angleEnable):
        """
        @brief Sets the angle calculation, magnetic gain, and offset corrections
         between two selected magnetic channels
        @param angleEnable value to write to the register for which angle calculation enabled
            0X0 = No angle calculation, magnitude gain, and offset
                   correction enabled
            0X1 = X 1st, Y 2nd
            0X2 = Y 1st, Z 2nd
            0X3 = X 1st, Z 2nd
            TMAG5273_REG_SENSOR_CONFIG_2 - bit 3-2
        @return Error code (0 is success, negative is failure, positive is warning)
        """
        if (angleEnable > TMAG5273_XZ_ANGLE_CALCULATION):
            raise f"Invalid angleEnable {hex(angleEnable)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, angleEnable, TMAG5273_ANGLE_CALCULATION_BITS, TMAG5273_ANGLE_CALCULATION_LSB)
            print(f"Setting angleEnable config to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2, mode)


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
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, lpLnMode, TMAG5273_LOW_POWER_BITS, TMAG5273_LOW_POWER_LSB)
            print(f"Setting low power mode config to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_2, mode)


    def setXYAxisRange(self, xyAxisRange):
        """
        @brief Sets the X and Y axes magnetic range from 2 different options
        @param xyAxisRange Value to choose the magnetic range
            0X0 = ±40mT, DEFAULT
            0X1 = ±80mT
            TMAG5273_REG_SENSOR_CONFIG_2 - bit 1
        @return Error code (0 is success, negative is failure, positive is warning)
        """
        if (xyAxisRange > TMAG5273_RANGE_80MT):
            raise f"Invalid xyAxisRange {hex(xyAxisRange)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, xyAxisRange, TMAG5273_XY_RANGE_BITS, TMAG5273_XY_RANGE_LSB)
            print(f"Setting xyAxisRange config to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2, mode)


    def setZAxisRange(self, zAxisRange):
        """
        @brief Sets the Z magnetic range from 2 different options
        @param zAxisRange Value to set the range from either 40mT or 80mT
            0X0 = ±40mT, DEFAULT
            0X1 = ±80mT
            TMAG5273_REG_SENSOR_CONFIG_2 - bit 0
        @return Error code (0 is success, negative is failure, positive is warning)
        """
        if (zAxisRange > TMAG5273_RANGE_80MT):
            raise f"Invalid zAxisRange {hex(zAxisRange)}"
        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2)
            mode = TMAG5273.setBitFieldValue(mode, zAxisRange, TMAG5273_Z_RANGE_BITS, TMAG5273_Z_RANGE_LSB)
            print(f"Setting zAxisRange config to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2, mode)


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
            deviceStatusReg = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_STATUS)
        return deviceStatusReg

    def getError(self):
        """Check the device status register to see if there is an issue"""
        statusReg = self.getDeviceStatus()
        if ((statusReg & (TMAG5273_DEVICE_STATUS_VCC_UV_ERROR_BITS | TMAG5273_DEVICE_STATUS_OTP_CRC_ERROR_BITS |
                        TMAG5273_DEVICE_STATUS_INT_ERROR_BITS | TMAG5273_OSCILLATOR_ERROR_BITS)) != 0):
            raise(f"Error detected. Status registry: {statusReg}")


    def getLowPower(self):
        """
        @brief Returns if the device is operating in low power
         or low noise mode.
            0X0 = Low active current mode
            0X1 = Low noise mode
            TMAG5273_REG_DEVICE_CONFIG_2 - bit 4
        @return Low power (0) or low noise (1) mode        
        """
        lowPowerMode = 0
        with SMBus(1) as bus:
            lowPowerMode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_2)
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
            opMode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_2)
        return TMAG5273.getBitFieldValue(opMode, TMAG5273_OPERATING_MODE_BITS, TMAG5273_OPERATING_MODE_LSB)


    def getMagneticChannel(self):
        """
        @brief Returns data acquisition from the following magnetic axis channels:
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
            TMAG5273_REG_SENSOR_CONFIG_1 - bit 7-4
        @return Code for the magnetic channel axis being read
        """
        magChannel = 0
        with SMBus(1) as bus:
            magChannel = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_1)
        return TMAG5273.getBitFieldValue(magChannel, TMAG5273_CHANNEL_MODE_BITS, TMAG5273_CHANNEL_MODE_LSB)


    def getTemperatureEN(self):
        """
        @brief Returns the enable bit that determines the data
         acquisition of the temperature channel.
            0x0 = Temp Channel Disabled
            0x1 = Temp Channel Enabled
            TMAG5273_REG_T_CONFIG - bit 0
        @return Enable bit that determines if temp channel is enabled or disabled
        """
        tempENreg = 0
        with SMBus(1) as bus:
            tempENreg = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_T_CONFIG)
        return TMAG5273.getBitFieldValue(tempENreg, TMAG5273_TEMPERATURE_BITS, TMAG5273_TEMPERATURE_LSB)


    def getAngleEn(self):
        """
        @brief Returns angle calculation, magnetic gain, and offset
         corrections between two selected magnetic channels.
            0X0 = No angle calculation, magnitude gain, and offset
                  correction enabled
            0X1 = X 1st, Y 2nd
            0X2 = Y 1st, Z 2nd
            0X3 = X 1st, Z 2nd
            TMAG5273_REG_SENSOR_CONFIG_2 - bit 3-2
        @return Angle calculation and associated channel order
        """
        angleReg = 0
        with SMBus(1) as bus:
            angleReg = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2)
        return TMAG5273.getBitFieldValue(angleReg, TMAG5273_ANGLE_CALCULATION_BITS, TMAG5273_ANGLE_CALCULATION_LSB)
    

    def getXYAxisRange(self):
        """
        @brief Returns the X and Y axes magnetic range from the
         two following options:
            0X0 = ±40mT, DEFAULT
            0X1 = ±80mT
            TMAG5273_REG_SENSOR_CONFIG_2 - bit 1
        @return X and Y axes magnetic range (0 or 1)
        """
        xyRangeReg = 0
        with SMBus(1) as bus:
            xyRangeReg = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_SENSOR_CONFIG_2)
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
        """
        @brief Reads back the X-Channel data conversion results, the
        MSB 8-Bit and LSB 8-Bits. This reads from the following registers:
            X_MSB_RESULT and X_LSB_RESULT
        @return X-Channel data conversion results        
        """
        dataBuffer = []
        with SMBus(1) as bus:
            dataBuffer = bus.read_i2c_block_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_X_MSB_RESULT, 2)
            xData = (dataBuffer[0] << 8) | dataBuffer[1]
            range = 40 if self.getXYAxisRange() == 0 else 80
            return self.calculateMagneticField(xData, range)
        
    
    def getYData(self):
        """
        @brief Reads back the Y-Channel data conversion results, the
         MSB 8-Bits and LSB 8-Bits. This reads from the following registers:
            Y_MSB_RESULT and Y_LSB_RESULT
        @return Y-Channel data conversion results        
        """
        dataBuffer = []
        with SMBus(1) as bus:
            dataBuffer = bus.read_i2c_block_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_Y_MSB_RESULT, 2)
            xData = (dataBuffer[0] << 8) | dataBuffer[1]
            range = 40 if self.getXYAxisRange() == 0 else 80
            return self.calculateMagneticField(xData, range)


    def getZData(self):
        """
        @brief Reads back the Z-Channel data conversion results, the
         MSB 8-Bits and LSB 8-Bits. This reads from the following registers:
            Z_MSB_RESULT and Z_LSB_RESULT
        @return Z-Channel data conversion results.        
        """
        dataBuffer = []
        with SMBus(1) as bus:
            dataBuffer = bus.read_i2c_block_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_Z_MSB_RESULT, 2)
            xData = (dataBuffer[0] << 8) | dataBuffer[1]
            range = 40 if self.getXYAxisRange() == 0 else 80
            return self.calculateMagneticField(xData, range)
        

    def getTemp(self):
        """
        @brief Reads back the T-Channel data conversion results,
         combining the MSB and LSB registers.
            T_MSB_RESULT and T_LSB_RESULT
        @return T-Channel data conversion results        
        """
        dataBuffer = []
        with SMBus(1) as bus:
            dataBuffer = bus.read_i2c_block_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_T_MSB_RESULT, 2)
            tData = (dataBuffer[0] << 8) | dataBuffer[1]
            return TMAG5273_TSENSE_T0 + ((tData - TMAG5273_TADC_T0) / TMAG5273_TADC_RES)
    

    def getAngleResult(self):
        """
        @brief Returns the angle measurement result in degree. The data
         displayed from 0 to 360 degree in 13 LSB bits after combining the
         MSB and LSB bits. The 4 LSB bits allocated for fraction of an angle
         in the format (xxx/16).
            TMAG5273_REG_ANGLE_RESULT_MSB
            TMAG5273_REG_ANGLE_RESULT_LSB
        @return Angle measurement result in degrees (float value)        
        """
        dataBuffer = []
        with SMBus(1) as bus:
            dataBuffer = bus.read_i2c_block_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_ANGLE_RESULT_MSB, 2)
            angleReg = (dataBuffer[0] << 8) | dataBuffer[1]
            fractionValue = (angleReg & 0xF) / 16.
            integerValue = (angleReg >> 4) & 0x1FF
            return integerValue + fractionValue
        
    
    def getMagnitudeResult(self):
        """
        @brief Returns the resultant vector magnitude (during angle
         measurement) result. This value should be constant during 360
         degree measurements.
        @return Vector magnitude during angle measurement        
        """
        magReg = 0
        with SMBus(1) as bus:
            magReg = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_MAGNITUDE_RESULT)
        return magReg
    

    def setConvAvg(self, avgMode):
        """
        @brief Sets the additional sampling of the sensor data to reduce the
        noise effect (or to increase resolution)
        @param avgMode value to set the conversion average
            0X0 = 1x average, 10.0-kSPS (3-axes) or 20-kSPS (1 axis)
            0X1 = 2x average, 5.7-kSPS (3-axes) or 13.3-kSPS (1 axis)
            0X2 = 4x average, 3.1-kSPS (3-axes) or 8.0-kSPS (1 axis)
            0X3 = 8x average, 1.6-kSPS (3-axes) or 4.4-kSPS (1 axis)
            0X4 = 16x average, 0.8-kSPS (3-axes) or 2.4-kSPS (1 axis)
            0X5 =  32x average, 0.4-kSPS (3-axes) or 1.2-kSPS (1 axis)
            TMAG5273_REG_DEVICE_CONFIG_1 - bit 4-2
        @return Error code (0 is success, negative is failure, positive is warning)
        """
        if (avgMode > TMAG5273_X32_CONVERSION):
            raise f"Inalid avgMode: {hex(avgMode)}"

        mode = 0
        with SMBus(1) as bus:
            mode = bus.read_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_1)
            mode = TMAG5273.setBitFieldValue(mode, avgMode, TMAG5273_CONV_AVG_BITS, TMAG5273_CONV_AVG_LSB)
            print(f"Setting conversion average to: {hex(mode)}")
            bus.write_byte_data(TMAG5273_I2C_ADDRESS_INITIAL, TMAG5273_REG_DEVICE_CONFIG_1, mode)
