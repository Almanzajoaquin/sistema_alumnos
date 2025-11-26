#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input

# FORZAR migraciones de todas las apps
python manage.py makemigrations usuarios
python manage.py makemigrations alumnos
python manage.py makemigrations scraper
python manage.py makemigrations
python manage.py migrate