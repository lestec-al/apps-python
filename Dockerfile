FROM ubuntu:latest

RUN apt update
RUN apt install python3 -y
RUN apt install python3-tk -y
RUN apt install python3-pip -y
RUN pip3 install send2trash
RUN mkdir -p /usr/app/src/data

WORKDIR /usr/app/src

COPY files_cl.py ./
COPY files_new.py ./
COPY files.ini ./
COPY data data/