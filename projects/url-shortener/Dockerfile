FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBUG=false

WORKDIR /app/url_shortener

COPY python/requirements.txt /app/requirements.txt
RUN python -m pip install --no-cache-dir -r /app/requirements.txt

COPY projects/url-shortener/ /app/url_shortener/

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn --bind 0.0.0.0:8000 --workers 2 --access-logfile - --error-logfile - wsgi:application"]

HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health/', timeout=2)" || exit 1
