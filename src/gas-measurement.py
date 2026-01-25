import time
import logging
import redis
from datetime import datetime
from enum import Enum
from TMAG5273_RaspberryPi_Library_Defs import *
from TMAG5273_RaspberryPi_Library import TMAG5273


logging.basicConfig(
    filename="gasLevel.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
)

class Period(Enum):
    SECOND = 1,
    DAY = 86400,
    WEEK = 86400*7,
    MONTH = 86400*30

sensor = TMAG5273()
tank_liters = 300

# redis documents
measurements_set = "measurements"
refills_set = "refills"


def double_to_date(time) -> str:
    return datetime.fromtimestamp(time).strftime('%d-%b-%Y %H:%M:%S')


def level_to_liters(level) -> int:
    return int((level/100) * tank_liters)


def is_refill(previous_measurement, current_measurement) -> bool:
    return current_measurement['level'] > previous_measurement['level'] + 10


def get_refill_liters(previous_measurement, current_measurement) -> int:
    diff = current_measurement['level'] - previous_measurement['level']
    return level_to_liters(diff)


def get_last_refill(r):
    latest_refill = r.zrevrange(measurements_set, 0, 0)
    return latest_refill


def calculate_avg_consumption(r, ts, period: Period) -> int:
    """in liters"""
    last_refill = get_last_refill(r)
    start_time = last_refill['time']
    start_level = last_refill['level']
    level_diff = start_level - level
    litters_diff = level_to_liters(level_diff)
    time_diff_seconds = ts - start_time
    time_diff_period = int(time_diff_seconds / period)
    return litters_diff / time_diff_period


def when_gas_will_be_empty(ts, liters, consumption_per_second):
    seconds_left = liters / consumption_per_second
    empty_time = ts + seconds_left
    return empty_time


try:
    sensor.begin()
    sensor.setConvAvg(TMAG5273_X32_CONVERSION)
    sensor.setMagneticChannel(TMAG5273_XYX_ENABLE)
    sensor.setAngleEn(TMAG5273_XY_ANGLE_CALCULATION)

    while True:
        sensor.setOperatingMode(TMAG5273_CONTINUOUS_MEASURE_MODE)
        level = sensor.getGasLevel()
        temperature = int(sensor.getTemp())
        logging.info(f"gasLevel: {level}")

        ts = int(time.time())
        key = f"measurement:{ts}"
        r = redis.Redis(host='localhost', port='6379', decode_responses=True)
        previous_measurement_key = r.zrevrange(measurements_set, 0, 0)[0]
        previous_measurement = r.json().get(previous_measurement_key)
        r.json().set(key, "$", { "time": ts, "time_as_text": double_to_date(ts), "temperature": temperature, "level": level, "liters": level_to_liters(level)})
        current_measurement = r.json().get(key)

        if (is_refill(previous_measurement, current_measurement)):
            liters = get_refill_liters(previous_measurement, current_measurement)
            refill_key = f"refill:{ts}"
            r.json().set(refill_key, "$", { "time": ts, "time_as_text": double_to_date(ts), "liters": liters, "level": level })
            r.zadd(refills_set, { refill_key: ts })
        
        r.zadd(measurements_set, { key: ts })

        sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)
        time.sleep(3600)

except KeyboardInterrupt:
    sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)