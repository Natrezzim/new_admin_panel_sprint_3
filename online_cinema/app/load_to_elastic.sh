#!/bin/sh

python /usr/src/app/postgres_to_elastic/main.py

exec "$@"