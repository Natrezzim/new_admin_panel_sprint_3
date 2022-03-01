FROM python:3.9-alpine

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && \
     apk add postgresql-dev gcc python3-dev musl-dev && \
     apk --no-cache add curl && \
     pip install --upgrade pip
COPY ../requirements.txt .
RUN pip install -r requirements.txt
COPY ./app ./app
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD sh -c "cd /usr/src/app/ && gunicorn config.wsgi:application --bind 0.0.0.0:8000"