FROM python:3.8.6

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    libspdlog-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/
RUN chmod -R 755 scripts

EXPOSE 8000

CMD ["./scripts/start_local.sh"]
