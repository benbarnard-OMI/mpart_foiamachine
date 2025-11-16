web: gunicorn foiamachine.config.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A foiamachine worker --loglevel=info
beat: celery -A foiamachine beat --loglevel=info
