Raspberry-Pi Gas

## Activate python venv
```
source .venv/bin/activate
```

## GIOZero Library
https://gpiozero.readthedocs.io/en/stable/

# Enable i2c ubuntu
```
sudo apt-get install i2c-tools
sudo i2cdetect -y 1 // The output should be a matrix of values

sudo nano /boot/firmware/config.txt
Update line from: `dtparam=i2c_arm=on` to `dtparam=i2c_arm=on,i2c_baudrate=115200`
sudo reboot // Reboot raspberry
```