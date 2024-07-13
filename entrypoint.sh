#!/bin/sh
set -ex

python -m flask run --host=0.0.0.0 --port=8010
