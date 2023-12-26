#!/bin/bash

pip install -r requirements.txt
python manage.py migrate
daphne travelmate_project.asgi:application  -b 0.0.0.0
