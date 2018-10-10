FROM ubuntu:18.04
COPY sources.list /etc/apt/

ARG KEY=default_key

RUN apt-get update \
    && apt-get install -y python3 python3-pip git vim

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple Django==2.1 \
    && pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

RUN cd /root \
    && git clone --single-branch -b deploy https://github.com/Botbattle-net/midware \
    && touch /root/midware/secretkey.py \
    && echo "secretKey = '$KEY'" >> /root/midware/secretkey.py \
    && mkdir /root/midware/log \
    && cd /root/midware \
    && python3 manage.py migrate --run-syncdb #bust the cache1

CMD cd /root/midware \
    && python3 manage.py runserver 0.0.0.0:8001 >> runserver.log