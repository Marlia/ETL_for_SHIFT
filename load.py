import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

df = pd.read_csv("weather.csv")
records = df.to_dict(orient='records')
conn = psycopg2.connect(
    host='db',
    dbname='weather',
    user='user',
    password='I_WANT_TO_SHIFT',
    port=5432
)
cur = conn.cursor()

columns = df.columns.tolist()
columns_str = ', '.join(columns)

sql = f"""
INSERT INTO weather_report ({columns_str})
VALUES %s
ON CONFLICT (date) DO UPDATE SET
{', '.join([f"{col}=EXCLUDED.{col}" for col in columns if col != 'date'])}
"""

values = [tuple(r[col] for col in columns) for r in records]

execute_values(cur, sql, values, page_size=100)

conn.commit()
cur.close()
conn.close()

print("Данные вставленны в базу")
