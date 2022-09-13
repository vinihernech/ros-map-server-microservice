FROM python:3.7-slim

SHELL [ "/bin/bash" , "-c" ]

RUN apt-get update

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install --upgrade protobuf==3.20.0 
RUN apt-get install -y python3-opencv
WORKDIR /opt/map_server/maps
WORKDIR /opt/map_server
COPY src/ .
COPY etc/ .


