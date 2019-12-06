#!/bin/bash
rm -rf blog/migrations/*
touch blog/migrations/__init__.py

python manage.py makemigrations
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.filter(email='administrator@example.com').delete(); User.objects.create_superuser('administrator@example.com', 'admin', 'admin')" | python manage.py shell
python manage.py runserver