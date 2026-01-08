import time
from TMAG5273_RaspberryPi_Library_Defs import *
from TMAG5273_RaspberryPi_Library import TMAG5273

print("")
print("------------------------------------------------------------------")
print("TMAG5273 Example 3: Angle Calculations")
print("------------------------------------------------------------------")
print("")

sensor = TMAG5273()
try:
    sensor.begin()
    sensor.setConvAvg(TMAG5273_X32_CONVERSION)
    sensor.setMagneticChannel(TMAG5273_XYX_ENABLE)
    sensor.setAngleEn(TMAG5273_XY_ANGLE_CALCULATION)

    while True:
        angleCalculation = sensor.getAngleResult()
        print(f"angleCalculation: {angleCalculation:.4f}")
        time.sleep(1)

except KeyboardInterrupt:
    sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)