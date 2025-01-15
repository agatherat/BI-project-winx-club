#!/bin/bash

DB_HOST="some-mysql"
DB_PORT=3306
DB_USER="root"
DB_PASSWORD="admin"
DB_NAME="prestashop"
DUMP_FILE="/tmp/sql/dump.sql"

echo "Waiting for MySQL to be ready..."
until mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1"; do
  echo "MySQL is not ready, waiting..."
  sleep 5
done

echo "Creating DB"
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"

echo "Initializing DB"
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < "$DUMP_FILE"

echo "Starting Server"
exec apache2-foreground
