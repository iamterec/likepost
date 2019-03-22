FROM python:3.6-alpine

RUN adduser -S celery_user

ENV CELERY_PATH /celery
RUN mkdir -p CELERY_PATH

WORKDIR $CELERY_PATH

#for psycopg2 installation
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
