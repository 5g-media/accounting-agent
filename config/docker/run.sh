#!/usr/bin/env bash

# Wait for postgres
while ! nc -z accounting_postgres 5432; do
  echo "Waiting for postgres server..."
  sleep 1
done

# Make migrations
cd /opt/accounting
python3 manage.py makemigrations api --settings=accounting.settings
python3 manage.py migrate --settings=accounting.settings
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@5gmedia.com', 'password')" | python3 manage.py shell --settings=accounting.settings

# Start supervisor
supervisord -c /etc/supervisor/supervisord.conf
update-rc.d supervisor defaults

# Start gunicorn
gunicorn accounting.wsgi:application

echo "Initialization completed."
tail -f /dev/null  # Necessary in order for the container to not stop
