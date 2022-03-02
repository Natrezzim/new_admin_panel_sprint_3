FROM python:3.9-alpine

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && \
    apk --no-cache add curl && \
     pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT sleep 30 && python /usr/src/main.py