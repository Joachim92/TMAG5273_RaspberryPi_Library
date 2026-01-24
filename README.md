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


# How to start redis instance
```
docker run --name redis -d -p 6379:6379 -v /home/joaramos/redis-data:/data --restart always redis redis-server --save 86400 1 --loglevel warning
```

# Connect to redis instance
```
docker exec -it redis redis-cli
```

# How to insert into redis using the cli
```
JSON.SET measurement:1769228195 $ '{ "date": "23-Jan-2026 22:40:13", "temperature": 23, "level": 70 }'
ZADD measurements 1769228195 measurement:1769228195
```
# query redis
```
ZRANGEBYSCORE measurements 1706040000 1769228195
JSON.GET measurement:1706042413

measurement_ids = r.zrangebyscore(sorted_set, 0, ts)
for id in measurement_ids:
    measurement = r.json().get(id)
    measurement['time'] = datetime.fromtimestamp(measurement['time']).strftime('%d-%b-%Y %H:%M:%S')
    print(measurement)
```

# delete redis
```
r.delete(sorted_set)
```

# What I want to know
- how much gas left
- when was the last time I filled the tank
    check the time in which the gasLevel changed from low to high by a lot (more than 10%)
    I can do this check after every new record is added in the db and update if needed
- how much gas I'm consuming per day/week/month
    This is calculated with the measurements data
- when will I need to refill
    This is calculated based on the daily/weekly consumption and how much gas is left
    Whenever a refill is detected, add it to the refills document

# questions I will be able to answer afterwards
- Am I consuming more gas than the average? By how much?
- Am I consuming more at certain times?
- Is it a lot when the boiler is on?
- Is it a lot when the dryer is on?
- Is it a lot when the stove is on?
- Is the gas being consumed when no one is using it?


# Data I want to store
tank: {
    "name": "house one",
    "capacity": 300,
}

consumption: {
    I don't think this is needed. I can calculate it based on the measurement values
}

refill: {
    "time": 1769228195,
    "liters": 120,
    "level": 40,
}

measurement {
  "time": 1769228195, // Stored as a double
  "temperature": 23,
  "level": 73,
}
