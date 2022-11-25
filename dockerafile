FROM ubuntu:20.04
WORKDIR /code

RUN apt-get update && apt-get install -y python3.9 python3.9-dev curl
RUN apt install git -y
RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python3-pip -y
RUN python3.9 -m pip install -U phonenumbers
RUN python3.9 -m pip install -U flask
RUN python3.9 -m pip install -U requests

COPY make.py make.py
RUN python3.9 make.py
COPY . .
EXPOSE 1000
CMD ["python3.9", "main.py"]
