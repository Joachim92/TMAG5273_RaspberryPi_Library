import time
from TMAG5273_RaspberryPi_Library_Defs import *
from TMAG5273_RaspberryPi_Library import TMAG5273

print("")
print("------------------------------------------------------------------")
print("TMAG5273 Example 1: Basic Readings")
print("------------------------------------------------------------------")
print("")

sensor = TMAG5273()
try:
    sensor.begin()
    sensor.setTemperatureEn(True)

    while True:
        magX = sensor.getXData()
        magY = sensor.getYData()
        magZ = sensor.getZData()
        temp = sensor.getTemp()

        print(f"Data -  Magnetic: [ X: {magX}, Y: {magY}, Z: {magZ} ] mT,   Temp: {temp} C")
        time.sleep(0.3)

except KeyboardInterrupt:
    sensor.setOperatingMode(TMAG5273_STANDBY_BY_MODE)