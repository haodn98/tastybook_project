FROM python:3.10-alpine

RUN mkdir -p /home/tastybook

ENV HOME=/home/tastybook
ENV APP_HOME=/home/tastybook/app
RUN mkdir $APP_HOME

WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . $APP_HOME

RUN chown -R tastybook:tastybook $APP_HOME

USER tastybook