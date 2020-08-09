#!/bin/bash

pip install --upgrade pip
pip install -r /app/requirements.txt

python migrate.py migrate all

gunicorn app:server -c /app/conf/gunicorn_conf.py --reload --log-level info
