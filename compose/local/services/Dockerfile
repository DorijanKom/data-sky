FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get install -y git postgresql zlib1g-dev libfreetype6-dev build-essential gettext libgettextpo-dev libpq-dev libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libffi-dev wget

COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/local/services/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/services/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/services/celery/worker/start /start-worker
RUN sed -i 's/\r//' /start-worker
RUN chmod +x /start-worker

COPY ./compose/local/services/celery/beat/start /start-beat
RUN sed -i 's/\r//' /start-beat
RUN chmod +x /start-beat


WORKDIR /app

ENTRYPOINT ["/entrypoint"]
