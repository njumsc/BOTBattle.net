FROM ubuntu:16.04
COPY sources.list /etc/apt/

RUN apt-get update \
    && apt-get install -y python3 python3-pip git vim

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Django \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

RUN cd /root \
    && git clone https://github.com/Botbattle-net/midware \
    && touch /root/midware/secretkey.py \
    && echo "secretKey = default_key" >> /root/midware/secretkey.py \
    && mkdir /root/midware/log \
    && cd /root/midware \
    && python3 manage.py migrate --run-syncdb #bust the cache

CMD cd /root/midware \
    && python3 manage.py runserver 0.0.0.0:8001 >> runserver.log