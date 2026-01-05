# TMAG5273 RaspberryPi Library

This is a python library for the Texas Instruments TMAG5273 low-power linear 3D Hall-effect sensor with I2C interface.

This is based on the [SparkFun TMAG5273 Arduino Library](https://github.com/sparkfun/SparkFun_TMAG5273_Arduino_Library).

## How to connect sensor to RaspberryPi

| Name |Pin | Qwiic Color |
| ----------- | ----------- | ----------- |
| 3.3v | 1 | red |
| SDA (Data) | 3 | blue |
| SCL (Clock) | 5 | yellow |
| GND | 9 | black |

[RaspberryPi Pinout](https://pinout.xyz/pinout/i2c)

## Ensure i2c is enabled and working
```
sudo apt-get install i2c-tools
sudo i2cdetect -y 1 // The output should be a matrix of values
```

## Setup Python project
From the main folder path execcute the following commands.
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install smbus2
pip3 install -e .
```

# Run an example
```
python3 examples/Example1_BasicReadings.py
```

## Additional References
[SparkFun Qwiic Hall Effect Sensor TMAG5273](https://docs.sparkfun.com/SparkFun_Qwiic_Hall_Effect_Sensor_TMAG5273/introduction/)


