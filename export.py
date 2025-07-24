import argparse
import psycopg2
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--start', required=True, help='Дата начала загрузки в формате YYYY-MM-DD')
parser.add_argument('--end', required=True, help='Дата конца загрузки в формате YYYY-MM-DD')
args = parser.parse_args()

conn = psycopg2.connect(
    host='db',
    dbname='weather',
    user='user',
    password='I_WANT_TO_SHIFT',
    port=5432
)

query = f"""
SELECT * 
FROM weather_report
WHERE date BETWEEN '{args.start}' AND '{args.end}'
ORDER BY date;
"""

df = pd.read_sql(query, conn)
df.to_csv(f"export_{args.start}_{args.end}.csv", index=False)

print(f"Данные сохранены в export_{args.start}_{args.end}.csv")
