#!/usr/bin/env bash
# Docker entrypoint script.

./manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
