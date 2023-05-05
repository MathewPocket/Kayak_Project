FROM  python:latest

WORKDIR /home/app

RUN apt-get update -y 
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt