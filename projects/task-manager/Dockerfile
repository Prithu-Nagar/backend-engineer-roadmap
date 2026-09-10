# Day 41 — Dockerize Task Manager
#
# Build from the repository root:
# docker build -f projects/task-manager/Dockerfile -t task-manager-api .
#
# Run:
# docker run --rm -p 5000:5000 task-manager-api

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/backend

COPY python/requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app/backend
COPY projects/task-manager /app/projects/task-manager

EXPOSE 5000

CMD ["python", "-c", "from app import app; app.run(host='0.0.0.0', port=5000)"]
