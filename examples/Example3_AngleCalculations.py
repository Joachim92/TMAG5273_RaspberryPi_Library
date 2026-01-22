import time
from TMAG5273_RaspberryPi_Library_Defs import *
from TMAG5273_RaspberryPi_Library import TMAG5273

print("")
print("------------------------------------------------------------------")
print("TMAG5273 Example 3: Angle Calculations")
print("------------------------------------------------------------------")
print("")

def map_value(x):
    points = [
        (360, 86),
        (300, 95),
        (235, 0),
        (201, 10),
        (177, 15),
        (160, 20),
        (146, 25),
        (131, 30),
        (122, 35),
        (110, 40),
        (100, 45),
        (91, 50),
        (79, 55),
        (69, 60),
        (57, 65),
        (45, 70),
        (31, 75),
        (16, 80),
        (0, 85),
    ]

    # Clamp to range
    if x >= points[0][0]:
        return points[0][1]
    if x <= points[-1][0]:
        return points[-1][1]

    # Find segment and interpolate
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        if x1 >= x >= x2:
            return int(y1 + (y2 - y1) * (x - x1) / (x2 - x1))


sensor = TMAG5273()
try:
    sensor.begin()
    sensor.setConvAvg(TMAG5273_X32_CONVERSION)
    sensor.setMagneticChannel(TMAG5273_XYX_ENABLE)
    sensor.setAngleEn(TMAG5273_XY_ANGLE_CALCULATION)

    while True:
        angleCalculation = sensor.getNormalizedAngleData()
        angle = map_value(angleCalculation)
        print(f"angleCalculation: {angleCalculation} -> angle {angle}")
        time.sleep(1)

except KeyboardInterrupt:
    sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)

# 235 -> 0
# 158 -> 20
# 91  -> 50
# 0   -> 85