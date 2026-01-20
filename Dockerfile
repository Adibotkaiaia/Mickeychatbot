FROM python:3.10-slim

RUN apt-get update -y && apt-get upgrade -y
RUN pip3 install -U pip

WORKDIR /app
COPY . /app

RUN pip3 install -U -r requirements.txt

CMD python3 main.py
