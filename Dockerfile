FROM python:3.7.3

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul

ADD requirements.txt /

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get update \
    && apt-get install -y libspdlog-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /var/cache/apt/archives \
    && mkdir /app

WORKDIR /app
COPY . /app/

EXPOSE 8000

CMD ["./scripts/start.sh"]
