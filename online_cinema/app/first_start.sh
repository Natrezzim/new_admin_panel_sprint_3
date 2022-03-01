#!/bin/sh

python app/manage.py flush --no-input
python app/manage.py migrate
python app/sqlite_to_postgres/load_data.py
pytest app/tests/check_consistency/test_load_data.py
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME','$DJANGO_SUPERUSER_EMAIL','$DJANGO_SUPERUSER_PASSWORD')" | python app/manage.py shell
rm -rf app/sqlite_to_postgres
rm -rf app/tests
rm -rf app/sqlscript
rm -rf app/movies_schema.sql
python app/manage.py collectstatic

exec "$@"