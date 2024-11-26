#!/bin/bash
lsof -i tcp:5000
find . -type d -name "__pycache__" -exec rm -r {} +
sleep 3
export PYTHONDONTWRITEBYTECODE=1
python3 run.py
