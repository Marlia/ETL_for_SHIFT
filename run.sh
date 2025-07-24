#!/bin/bash

set -e

DB_CONTAINER=weather_db
PY_CONTAINER=weather_etl
DB_NAME=weather
DB_USER=user
SQL_FILE=create_table.sql

echo "Запуск docker-compose"
docker-compose up -d --build

echo "Создание таблицы"
docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME < $SQL_FILE

read -p "Введите дату начала загрузки в формате YYYY-MM-DD: " START_DATE
read -p "Введите дату конца загрузки в формате YYYY-MM-DD: " END_DATE

docker exec -it $PY_CONTAINER python extract.py --start $START_DATE --end $END_DATE

docker exec -it $PY_CONTAINER python transform.py

echo "Загрузка CSV в базу данных"
docker exec -it $PY_CONTAINER python load.py

echo "Готово!"
