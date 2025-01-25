#!/bin/sh
set -ex

# python -m flask run --host=0.0.0.0
gunicorn --bind 0.0.0.0:5001 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker app:app

