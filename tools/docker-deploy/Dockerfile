FROM ubuntu:16.04
COPY sources.list /etc/apt/

RUN apt-get update \
    && apt-get install -y build-essential python3 python3-pip git vim

RUN pip install Django \
    && cd /root \
    && git clone https://github.com/Botbattle-net/midware \
    && touch /root/midware/secretkey.py \
    && echo "secretKey = " >> /root/midware/secretkey.py