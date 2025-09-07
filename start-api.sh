#!/bin/bash

cd /home/askcos/infra
/home/askcos/.local/bin/uv sync
/home/askcos/.local/bin/uv run fastapi run --host 127.0.0.1 --port 11000 --app app cheminfra/api/server.py
