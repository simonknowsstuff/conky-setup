import json
import requests
import statistics
import shutil
import time
from pathlib import Path

REQUEST_URL = "https://api.open-meteo.com/v1/forecast"
MAIN_DIRECTORY = Path(__file__).parent.resolve()
WEATHER_ICON_DIRECTORY = f"{MAIN_DIRECTORY}/weather-icons/"
OUTPUT_SVG = f"{MAIN_DIRECTORY}/weather_current.svg"
LATTITUDE = 0.0
LONGITUDE = 0.0

with open(f'{MAIN_DIRECTORY}/lat_lon.txt', 'r') as file:
    lines = [line.rstrip() for line in file]
    LATITUDE = float(lines[0])
    LONGITUDE = float(lines[1])

REQUEST_PARAMS = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "daily": {"temperature_2m_max", "temperature_2m_min"},
    "timezone": "GMT",
    "current_weather": "true"
}



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
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/01{day_code}.svg", OUTPUT_SVG)
        return "Clear Sky"
    elif code in [1, 2, 3]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/02{day_code}.svg", OUTPUT_SVG)
        return "Partly cloudy"
    elif code in [45, 48]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/50{day_code}.svg", OUTPUT_SVG)
        return "Fog"
    elif code in [51, 53, 55]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/10{day_code}.svg", OUTPUT_SVG)
        return "Drizzle"
    elif code in [56, 57]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/10{day_code}.svg", OUTPUT_SVG)
        return "Freezing drizzle"
    elif code in [61, 63, 65]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/10{day_code}.svg", OUTPUT_SVG)
        return "Rain"
    elif code in [66, 67]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/10{day_code}.svg", OUTPUT_SVG)
        return "Freezing rain"
    elif code in [71, 73, 75]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/13{day_code}.svg", OUTPUT_SVG)
        return "Slight snow fall"
    elif code == 77:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/13{day_code}.svg", OUTPUT_SVG)
        return "Snow grains"
    elif code in [80, 81, 82]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/10{day_code}.svg", OUTPUT_SVG)
        return "Rain showers"
    elif code in [85, 86]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/13{day_code}.svg", OUTPUT_SVG)
        return "Snow showers"
    elif code == 95:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/11{day_code}.svg", OUTPUT_SVG)
        return "Slight thunderstorm"
    elif code in [96, 99]:
        shutil.copy2(f"{WEATHER_ICON_DIRECTORY}/11{day_code}.svg", OUTPUT_SVG)
        return "Thunderstorm"


def main():
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

main()
