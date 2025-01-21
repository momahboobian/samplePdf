#!/bin/sh
set -ex

# python -m flask run --host=0.0.0.0
# gunicorn -w 4 -b 0.0.0.0:$PORT app:app
gunicorn -w 4 -b 0.0.0.0:5001 -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker app:app
# uwsgi --http :5000 --wsgi-file app.py --callable app

