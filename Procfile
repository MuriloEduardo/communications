web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A core worker -l INFO -Q ai-postprocessing
