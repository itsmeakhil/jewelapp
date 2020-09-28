#!/usr/bin/env bash
# start-server.sh
(cd jewelapp; python manage.py collectstatic --noinput; gunicorn jewelapp.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3) &
nginx -g "daemon off;"
