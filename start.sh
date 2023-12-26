#!/bin/bash

pip install -r requirements.txt
pip list
python manage.py migrate
daphne travelmate_project.asgi:application  -b 0.0.0.0
