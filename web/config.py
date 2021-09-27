#!/usr/bin/env python3

import os

LOG_LEVEL = 'INFO'
DEBUG = True
ENV = 'development'

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'worfometer.sqlite')
