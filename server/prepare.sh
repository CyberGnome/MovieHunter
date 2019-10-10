#!/usr/bin/env bash

PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -U postgres -c "DROP DATABASE moviedb;"
PGPASSWORD=postgres psql -h 127.0.0.1 -p 5432 -U postgres -c "CREATE DATABASE moviedb;"
