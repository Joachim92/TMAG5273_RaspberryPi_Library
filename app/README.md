# Fastapi

# TODO
Design alerts if:
 - 1.2–1.5 kg/day
 - Sudden drops
 - Night-time consumption

# Start
```
// for dev
fastapi dev app/main.py
//for production
fastapi run app/main.py
```

# How to run the service
```
sudo systemctl status gas-fastapi
sudo systemctl enable gas-fastapi
sudo systemctl start gas-fastapi
sudo systemctl stop gas-fastapi
sudo systemctl disable gas-fastapi
```

# Measurement
1 liter ≈ 0.54 kg

full tank = 240 L = 80 % = 130 kg


Typical consumption family home
    0.6 – 1.0 kg/day
    18 – 30 kg/month

Normal usage:
    130 kg ÷ 0.8 kg/day ≈ 160 days

Higher usage (long showers, many people):
    130 kg ÷ 1.2 kg/day ≈ 108 days

Red flag zone:
    If it lasts < 3 months, something’s off:
     - Leak
     - Inefficient heater
     - Excessive hot water use