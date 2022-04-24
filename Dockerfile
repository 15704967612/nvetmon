FROM python:3.8-alpine

#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && apk add --update --no-cache gcc musl-dev libc-dev libffi-dev linux-headers postgresql-dev


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

#RUN pip3 config set global.index-url https://mirrors.aliyun.com/pypi/simple
#RUN pip3 config set install.trusted-host mirrors.aliyun.com
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "gunicorn", "-c", "gun.py", "app:app" ]
