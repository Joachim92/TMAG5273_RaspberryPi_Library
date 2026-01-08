
# TMAG5273 RaspBerryPi Library

This is a Python library for the Texas Instruments TMAG5273 low-power linear 3D Hall-effect sensor with I<sup>2</sup>C interface.

![GitHub License](https://img.shields.io/github/license/sparkfun/SparkFun_TMAG5273_Arduino_Library)

This Library for the Texas Instruments TMAG5273 linear 3D Hall-effect sensor provides access to the core functionality of the sensor. The sensor itself includes three Hall-effect sensors, providing readings around the X, Y and Z axes of the device.

## Functionality

 SparkFun Arduino Library for the TMAG5273 provides access to the a majority of the functionality provided by the the TMAG5273 device. This includes:

- Access to X, Y and Z Hall-effect sensor readings
- Data digitized via an integrated 12-bit ADC
- Integrated temperature sensor
- Configurable to enable any combination of magnetic axes and temperature measurements
- Integrated angle calculation engine (CORDIC) provides full 360 degree position information
- Magnetic gain and offset correction settings
- Configurable I2C address, with a default value of `0x22`

## How to connect sensor to RaspberryPi

| Name |Pin | Qwiic Color |
| ----------- | ----------- | ----------- |
| 3.3v | 1 | red |
| SDA (Data) | 3 | blue |
| SCL (Clock) | 5 | yellow |
| GND | 9 | black |

[RaspberryPi Pinout](https://pinout.xyz/pinout/i2c)

## Using the Library

### Ensure i2c is enabled and working
Use the following commands in the terminal, if it is enabled, the output should be a matrix of values.
```
sudo apt-get install i2c-tools
sudo i2cdetect -y 1
```

### Setup Python project
From the main folder path execcute the following commands. This will create a new virtual environment and install the dependencies.
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install smbus2
pip3 install -e .
```

### Run an example
The examples print values in the terminal window.
```
python3 examples/Example1_BasicReadings.py
```

## Documentation

|Reference | Description |
|---|---|
|[SparkFun Hall-Effect Sensor - TMAG5273](https://github.com/sparkfun/SparkFun_Qwiic_Hall_Effect_Sensor_TMAG5273)| Hardware GitHub Repository|
|[Hall-Effect Sensor Hook Up Guide](https://docs.sparkfun.com/SparkFun_Qwiic_Hall_Effect_Sensor_TMAG5273) | Hardware Overview and Quick Start for the SparkFun Hall-Effect Sensor - TMAG5273 |

## License Information

This product is ***open source***!

This product is licensed using the [MIT Open Source License](https://opensource.org/license/mit).
