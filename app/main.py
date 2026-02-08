# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis
from enum import Enum
from datetime import datetime
import time

# redis documents
measurements_set = "measurements"
refills_set = "refills"

tank_liters = 300

class Period(Enum):
    SECOND = 1
    DAY = 86400
    WEEK = 86400*7
    MONTH = 86400*30

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


def double_to_date(time) -> str:
    return datetime.fromtimestamp(time).strftime('%d-%b-%Y %H:%M:%S')


def get_dummy_measurement():
    ts = time.time()
    return { 
        "time": ts,
        "time_as_text": double_to_date(ts),
        "temperature": 20,
        "level": 80,
        "liters": 240
    }


def get_dummy_refill():
    ts = time.time()
    return {
        "time": ts,
        "time_as_text": double_to_date(ts), 
        "level": 80,
        "liters": 240
    }


def get_latest_refill(r):
    refills = r.zrevrange(refills_set, 0, 0)
    if not refills:
        return get_dummy_refill()
    latest_refill_key = refills[0]
    latest_refill = r.json().get(latest_refill_key)
    return latest_refill


def level_to_liters(level) -> int:
    return int((level/100) * tank_liters)


def get_latest_measurement(r):
    measurements = r.zrevrange(measurements_set, 0, 0)
    if not measurements:
        return get_dummy_measurement()
    latest_measurement_key = measurements[0]
    latest_measurement = r.json().get(latest_measurement_key)
    return latest_measurement


def calculate_avg_consumption(latest_refill, latest_measurement, period: Period) -> int:
    """in liters"""
    start_time = latest_refill['time']
    start_level = latest_refill['level']
    level_diff = start_level - latest_measurement['level']
    litters_diff = level_to_liters(level_diff)
    time_diff_seconds = latest_measurement['time'] - start_time
    time_diff_period = time_diff_seconds / period.value

    if time_diff_period == 0:
        return 0
    return (litters_diff) / time_diff_period


def when_gas_will_be_empty(ts, liters, consumption_per_second):
    if consumption_per_second == 0:
        return "Not enough data"
    seconds_left = liters / consumption_per_second
    empty_time = ts + seconds_left
    return datetime.fromtimestamp(empty_time).strftime('%d-%b-%Y')


def get_measurements_since_last_refill(r, latest_refill, latest_measurement) -> list:
    measurement_ids = r.zrangebyscore(measurements_set, latest_refill['time'], latest_measurement['time'])
    measurements = []
    seen_days = set()

    for id in measurement_ids:
        measurement = r.json().get(id)
        day = datetime.fromtimestamp(measurement['time']).date()
        if day not in seen_days:
            seen_days.add(day)
            measurements.append(measurement)
    return measurements


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    r = redis.Redis(host='localhost', port='6379', decode_responses=True)
    latest_refill = get_latest_refill(r)
    latest_measurement = get_latest_measurement(r)
    average_consumption = calculate_avg_consumption(latest_refill, latest_measurement, Period.SECOND)
    gas_empty_on = when_gas_will_be_empty(latest_measurement['time'], latest_measurement['liters'], average_consumption)
    measurements = get_measurements_since_last_refill(r, latest_refill, latest_measurement)
    labels = [m["time_as_text"][:6] for m in measurements]
    values = [m["level"] for m in measurements]

    r.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "latest_measurement": latest_measurement,
            "latest_refill": latest_refill,
            "average_consumption": average_consumption,
            "gas_empty_on": gas_empty_on,
            "measurements": measurements,
            "labels": labels,
            "values": values
        }
    )