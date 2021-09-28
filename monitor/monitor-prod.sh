#!/bin/bash

readonly script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

source "$script_dir/.venv/bin/activate"
python3 "$script_dir/worfometer.py"
