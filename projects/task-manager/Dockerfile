# Day 45 — Deployment-ready Task Manager
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

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
