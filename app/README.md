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

# Compile postcss
npx postcss app/static/style.css -o app/static/style.out.css

# AI Prompt
I've this project:

    app
        static
            style.css
        templates
            index.html
        main.py
        postcss.config.js

The project is ran with this command 'fastapi dev main.py'

This is the content of 'postcss.config.js'

export default {
  plugins: {
    "@tailwindcss/postcss": {},
  }
}

main.py has this:

app.mount("/static", StaticFiles(directory="static"), name="static")

in the index.html I've this:

<link rel="stylesheet" href="/static/style.css">

what am I missing to have tailwind loaded? I'm trying to use postcss