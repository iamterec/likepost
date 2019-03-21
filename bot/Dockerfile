FROM python:3.6-alpine

ENV INSTALL_PATH /bot
RUN mkdir -p INSTALL_PATH 

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
