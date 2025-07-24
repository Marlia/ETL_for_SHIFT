import json
import pandas as pd
import numpy as np
from datetime import datetime

def f_to_c(f): return (f - 32) * 5 / 9
def kn_to_mps(kn): return kn * 0.514444
def inch_to_mm(inch): return inch * 25.4
def seconds_to_hours(sec): return sec / 3600


from datetime import timezone

def unixtime_to_iso(ts): return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()

with open("open_meteo.json") as f:
    data = json.load(f)

hourly = pd.DataFrame(data['hourly'])
daily = pd.DataFrame(data['daily'])

hourly['time'] = pd.to_datetime(hourly['time'], unit='s')
daily['time'] = pd.to_datetime(daily['time'], unit='s')
daily['sunrise'] = pd.to_datetime(daily['sunrise'], unit='s')
daily['sunset'] = pd.to_datetime(daily['sunset'], unit='s')

hourly['date'] = hourly['time'].dt.date
daily['date'] = daily['time'].dt.date

temp_cols = ['temperature_2m', 'dew_point_2m', 'apparent_temperature',
             'temperature_80m', 'temperature_120m',
             'soil_temperature_0cm', 'soil_temperature_6cm']

for col in temp_cols:
    hourly[col] = f_to_c(hourly[col])

for col in ['wind_speed_10m', 'wind_speed_80m']:
    hourly[col] = kn_to_mps(hourly[col])

for col in ['rain', 'showers', 'snowfall']:
    hourly[col] = inch_to_mm(hourly[col])

hourly['visibility'] = hourly['visibility'] * 0.3048  # ft → m

daily_agg = (
    hourly.groupby('date').agg({
        'temperature_2m': 'mean',
        'relative_humidity_2m': 'mean',
        'dew_point_2m': 'mean',
        'apparent_temperature': 'mean',
        'temperature_80m': 'mean',
        'temperature_120m': 'mean',
        'wind_speed_10m': 'mean',
        'wind_speed_80m': 'mean',
        'visibility': 'mean',
        'rain': 'sum',
        'showers': 'sum',
        'snowfall': 'sum'
    }).reset_index()
)

daily_agg.columns = ['date'] + [
    f'avg_{col}_24h' if stat == 'mean' else f'total_{col}_24h'
    for col, stat in zip(daily_agg.columns[1:], ['mean'] * 9 + ['sum'] * 3)
]

result_rows = []

for _, day in daily.iterrows():
    date = day['date']
    sunrise = day['sunrise']
    sunset = day['sunset']

    mask = (hourly['time'] >= sunrise) & (hourly['time'] <= sunset)
    daylight = hourly[mask]

    row = {
        'date': date,
        'daylight_hours': round(seconds_to_hours(day['daylight_duration']), 2),
        'sunrise_iso': unixtime_to_iso(int(day['sunrise'].timestamp())),
        'sunset_iso': unixtime_to_iso(int(day['sunset'].timestamp()))
    }

    for col in ['temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
                'apparent_temperature', 'temperature_80m', 'temperature_120m',
                'wind_speed_10m', 'wind_speed_80m', 'visibility']:
        row[f'avg_{col}_daylight'] = daylight[col].mean()

    for col in ['rain', 'showers', 'snowfall']:
        row[f'total_{col}_daylight'] = daylight[col].sum()

    result_rows.append(row)

daylight_agg = pd.DataFrame(result_rows)

soil_temps = (
    hourly.groupby('date')[['soil_temperature_0cm', 'soil_temperature_6cm']]
    .mean()
    .reset_index()
    .rename(columns={
        'soil_temperature_0cm': 'soil_temperature_0cm_celsius',
        'soil_temperature_6cm': 'soil_temperature_6cm_celsius'
    })
)


final_df = daily_agg.merge(daylight_agg, on='date', how='left')
final_df = final_df.merge(soil_temps, on='date', how='left')

final_df['wind_speed_10m_m_per_s'] = final_df['avg_wind_speed_10m_24h']
final_df['wind_speed_80m_m_per_s'] = final_df['avg_wind_speed_80m_24h']

final_df['temperature_2m_celsius'] = final_df['avg_temperature_2m_24h']
final_df['apparent_temperature_celsius'] = final_df['avg_apparent_temperature_24h']
final_df['temperature_80m_celsius'] = final_df['avg_temperature_80m_24h']
final_df['temperature_120m_celsius'] = final_df['avg_temperature_120m_24h']

final_df['rain_mm'] = final_df['total_rain_24h']
final_df['showers_mm'] = final_df['total_showers_24h']
final_df['snowfall_mm'] = final_df['total_snowfall_24h']

namedf = "weather.csv"
final_df.to_csv(namedf, index=False)
print(f"Файл .json преобразован и сохранён в {namedf}")
