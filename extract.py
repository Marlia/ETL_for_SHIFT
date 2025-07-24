import argparse
import requests
import json

parser = argparse.ArgumentParser()
parser.add_argument('--start', required=True, help='Формат даты YYYY-MM-DD')
parser.add_argument('--end', required=True, help='Формат даты YYYY-MM-DD')
args = parser.parse_args()

latitude = 55.0344
longitude = 82.9434

url = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={latitude}&longitude={longitude}"
    f"&daily=sunrise,sunset,daylight_duration"
    f"&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,"
    f"apparent_temperature,temperature_80m,temperature_120m,"
    f"wind_speed_10m,wind_speed_80m,wind_direction_10m,wind_direction_80m,"
    f"visibility,evapotranspiration,weather_code,soil_temperature_0cm,"
    f"soil_temperature_6cm,rain,showers,snowfall"
    f"&timezone=auto&timeformat=unixtime"
    f"&wind_speed_unit=kn&temperature_unit=fahrenheit"
    f"&precipitation_unit=inch"
    f"&start_date={args.start}&end_date={args.end}"
)

response = requests.get(url)
data = response.json()

with open("open_meteo.json", "w") as f:
    json.dump(data, f, indent=2)

print("Данные сохранены в open_meteo.json")