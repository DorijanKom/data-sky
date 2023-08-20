FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y git postgresql zlib1g-dev libfreetype6-dev build-essential gettext libgettextpo-dev libpq-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libffi-dev wget

COPY ./requirements /requirements
RUN pip install -r /requirements/staging.txt

COPY ./compose/local/services/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/services/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/services/celery/worker/start /start-worker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/services/celery/beat/start /start-beat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat


WORKDIR /app

ENTRYPOINT ["/entrypoint"]
