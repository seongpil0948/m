FROM python:3.8.6

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    libspdlog-dev \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/
RUN chmod -R 755 scripts

# setup all the configfiles
RUN echo "deamon off;" >> /etc/nginx/nginx.conf


EXPOSE 8000

CMD ["./scripts/start_local.sh"]
