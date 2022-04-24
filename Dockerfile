FROM python:3.8-alpine

RUN apk add tzdata && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && apk del tzdata

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 config set global.index-url http://mirrors.aliyun.com/pypi/simple
RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "gunicorn", "-c", "gun.py", "app:app" ]
