#!/bin/bash

set -e
set -u

function create_user_and_database() {
  local database=$1
  echo "  Creating user and database '$database'"
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
      CREATE DATABASE $database;
      GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" -d $database <<-EOSQL
      CREATE EXTENSION postgis;
EOSQL
}

if [ -n "$DATABASES" ]; then
  echo "Multiple database creation requested: $DATABASES"
  for db in $(echo $DATABASES | tr ',' ' '); do
    create_user_and_database $db
  done
  echo "Multiple databases created"
fi
