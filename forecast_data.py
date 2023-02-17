import json
import requests
import statistics
import shutil
import time
from pathlib import Path


def check_day():
    current_time = time.localtime()
    if current_time.tm_hour < 6 or current_time.tm_hour > 18:
        return False
    else:
        return True


def weather_code(code: int, is_day: bool):
    day_code = 'd'
    if not is_day:
        day_code = 'n'
    if code == 0:
        shutil.copy2(f"weather-icons/01{day_code}.svg", "weather_current.svg")
        return "Clear Sky"
    elif code in [1, 2, 3]:
        shutil.copy2(f"weather-icons/02{day_code}.svg", "weather_current.svg")
        return "Partly cloudy"
    elif code in [45, 48]:
        shutil.copy2(f"weather-icons/50{day_code}.svg", "weather_current.svg")
        return "Fog"
    elif code in [51, 53, 55]:
        shutil.copy2(f"weather-icons/10{day_code}.svg", "weather_current.svg")
        return "Drizzle"
    elif code in [56, 57]:
        shutil.copy2(f"weather-icons/10{day_code}.svg", "weather_current.svg")
        return "Freezing drizzle"
    elif code in [61, 63, 65]:
        shutil.copy2(f"weather-icons/10{day_code}.svg", "weather_current.svg")
        return "Rain"
    elif code in [66, 67]:
        shutil.copy2(f"weather-icons/10{day_code}.svg", "weather_current.svg")
        return "Freezing rain"
    elif code in [71, 73, 75]:
        shutil.copy2(f"weather-icons/13{day_code}.svg", "weather_current.svg")
        return "Slight snow fall"
    elif code == 77:
        shutil.copy2(f"weather-icons/13{day_code}.svg", "weather_current.svg")
        return "Snow grains"
    elif code in [80, 81, 82]:
        shutil.copy2(f"weather-icons/10{day_code}.svg", "weather_current.svg")
        return "Rain showers"
    elif code in [85, 86]:
        shutil.copy2(f"weather-icons/13{day_code}.svg", "weather_current.svg")
        return "Snow showers"
    elif code == 95:
        shutil.copy2(f"weather-icons/11{day_code}.svg", "weather_current.svg")
        return "Slight thunderstorm"
    elif code in [96, 99]:
        shutil.copy2(f"weather-icons/11{day_code}.svg", "weather_current.svg")
        return "Thunderstorm"


REQUEST_PARAMS = {
    "latitude": 53.83766,
    "longitude": -9.35136,
    "daily": {"temperature_2m_max", "temperature_2m_min"},
    "timezone": "GMT",
    "current_weather": "true",
    "timeformat": "unixtime"
}
REQUEST_URL = "https://api.open-meteo.com/v1/forecast"
MAIN_DIRECTORY = Path(__file__).parent.resolve()

response = requests.get(REQUEST_URL, params=REQUEST_PARAMS)
if response.status_code == 200:
    resp_data = response.json()
    data = {
        "temp": resp_data['current_weather']['temperature'],
        "max_temp": statistics.mean(resp_data['daily']['temperature_2m_max']),
        "min_temp": statistics.mean(resp_data['daily']['temperature_2m_min']),
        "weather": weather_code(resp_data['current_weather']['weathercode'], check_day())
    }
    with open(f'{MAIN_DIRECTORY}/forecast.json', 'w') as file:
        file.writelines(json.dumps(data))
        file.close()
