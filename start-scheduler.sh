#!/bin/bash

cd /home/askcos/infra
/home/askcos/.local/bin/uv sync
/home/askcos/.local/bin/uv run python main.py scheduler
