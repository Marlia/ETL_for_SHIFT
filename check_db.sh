#!/bin/bash

set -e

DB_CONTAINER=weather_db
DB_NAME=weather
DB_USER=user

docker exec -it $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "\dt"

docker exec -it $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -c "SELECT COUNT(*) FROM weather_report;"

docker exec -it $DB_CONTAINER psql -U $DB_USER -d $DB_NAME -P expanded=on -c "SELECT * FROM weather_report LIMIT 5;"

