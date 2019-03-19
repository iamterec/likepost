FROM python:3.6-alpine

ENV INSTALL_PATH /likepost
RUN mkdir -p INSTALL_PATH 

WORKDIR $INSTALL_PATH

#for psycopg2 installation
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
