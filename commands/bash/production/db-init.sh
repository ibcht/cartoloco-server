#!/bin/bash

source "${0%/*}/env"
"${0%/*}/activate.sh"
flask db:init
