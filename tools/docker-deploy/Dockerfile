FROM ubuntu:16.04
COPY sources.list /etc/apt/

RUN apt-get update \
    && apt-get install -y build-essential python3 python3-pip git vim

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Django \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests \
    && cd /root \
    && git clone https://github.com/Botbattle-net/midware \
    && touch /root/midware/secretkey.py \
    && echo "secretKey = default_key" >> /root/midware/secretkey.py \
    && mkdir /root/midware/log

