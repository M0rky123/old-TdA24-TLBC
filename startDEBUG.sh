#!/bin/sh

python3 -m flask --app app/app.py init-db
python3 -m flask --app app/app.py run --debug
