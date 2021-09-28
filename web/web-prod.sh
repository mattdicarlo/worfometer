#!/bin/bash

readonly script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Active the virtualenv for the project.
source "$script_dir/.venv/bin/activate"

gunicorn --bind 'unix:/tmp/gunicorn.sock' --workers 2 'app:create_app()'
