# ETL_for_SHIFT
Задание на позицию DE.
Для автоматического запуска всех программ нужно выполнить скрипт run.sh

Скрипт выполняет следующие команды в данном порядке:

set -e
DB_CONTAINER=weather_db
PY_CONTAINER=weather_etl
DB_NAME=weather
DB_USER=user
SQL_FILE=create_table.sql
docker-compose up -d --build
docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME < $SQL_FILE
read -p "Введите дату начала загрузки в формате YYYY-MM-DD: " START_DATE
read -p "Введите дату конца загрузки в формате YYYY-MM-DD: " END_DATE
docker exec -it $PY_CONTAINER python extract.py --start $START_DATE --end $END_DATE
docker exec -it $PY_CONTAINER python transform.py
docker exec -it $PY_CONTAINER python load.py


После запуска скрипта начинается автоматическая сборка и запуск Docker-контейнеров. В первом из них поднимается PostgreSQL, а во втором среда для выполнения Python-скриптов.

Затем создаётся таблица в базе данных, если она ещё не существует. После этого нужно вручную ввести диапазон дат, за который нужно получить погодные данные.
Загруженные данные преобразуются и сохранятся в CSV-файл, который автоматически загрузится в таблицу БД.

Для выгрузки данных используйте следующую команду:
docker exec -it weather_etl python export.py --start 2025-05-16 --end 2025-05-30


ПРИ ОТСУТСТВИИ BASH ДЛЯ ЗАПУСКА СКРИПТА, вводите команды скрипта вручную в том же порядке.
