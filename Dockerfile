FROM python:3.8-alpine

WORKDIR /app

RUN apk add --update --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add --update --no-cache gcc musl-dev libc-dev libffi-dev linux-headers \
    && apk add telegraf

#RUN apk add --update --no-cache gcc musl-dev libc-dev libffi-dev linux-headers postgresql-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt


COPY . /app

ENTRYPOINT [ "gunicorn", "-c", "gun.py", "app:app" ]
