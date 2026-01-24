import time
import logging
import redis
from datetime import datetime
from TMAG5273_RaspberryPi_Library_Defs import *
from TMAG5273_RaspberryPi_Library import TMAG5273

# send gasLevel to a redis instance

logging.basicConfig(
    filename="gasLevel.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%b-%Y %H:%M:%S",
)


# sensor = TMAG5273()
# try:
#     sensor.begin()
#     sensor.setConvAvg(TMAG5273_X32_CONVERSION)
#     sensor.setMagneticChannel(TMAG5273_XYX_ENABLE)
#     sensor.setAngleEn(TMAG5273_XY_ANGLE_CALCULATION)

#     while True:
#         sensor.setOperatingMode(TMAG5273_CONTINUOUS_MEASURE_MODE)
#         level = sensor.getGasLevel()
#         logging.info(f"gasLevel: {level}")
#         sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)
#         time.sleep(2)

# except KeyboardInterrupt:
#     sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)

sorted_set = "measurements"
ts = int(time.time())
key = f"measurement:{ts}"

r = redis.Redis(host='localhost', port='6379', decode_responses=True)

# r.delete(sorted_set)
# for i in range(0,10):
#     r.json().set(f"measurement:{ts+i}", "$", { "time": ts + 86400*i, "temperature": 23, "level": 80-i })
#     r.zadd(sorted_set, { f"measurement:{ts+i}": ts })

measurement_ids = r.zrangebyscore(sorted_set, 1706040000, ts)
consumption = 0

for id in measurement_ids:
    measurement = r.json().get(id)
    measurement['time'] = datetime.fromtimestamp(measurement['time']).strftime('%d-%b-%Y %H:%M:%S')
    print(measurement)