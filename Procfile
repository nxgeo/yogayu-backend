release: python manage.py migrate --no-input
web: python -m gunicorn yogayurest.asgi:application -k uvicorn_worker.UvicornWorker