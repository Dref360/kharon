#!/usr/bin/with-contenv bash
echo $(env)
. /app/venv/bin/activate && python3 /app/main.py