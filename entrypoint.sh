#!/bin/bash

cd /app
.venv/bin/python -m alembic upgrade head
cd ..
/app/.venv/bin/python -m uvicorn src.app:app --host 0.0.0.0 --port 5000