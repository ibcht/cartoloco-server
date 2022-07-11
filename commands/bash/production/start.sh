#!/bin/bash

source "${0%/*}/env"
"${0%/*}/activate.sh"
gunicorn -w 4 'tchou:create_app()'
