#!/bin/bash

source "${0%/*}/env"
"${0%/*}/activate.sh"
pip install gunicorn

