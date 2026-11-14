FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/expense-tracker

WORKDIR /app
RUN python -m pip install --no-cache-dir SQLAlchemy==2.0.54

COPY projects/expense-tracker /app/expense-tracker

WORKDIR /app/expense-tracker
CMD ["python", "demo.py"]
