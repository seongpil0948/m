FROM python:3.8.6

ENV PYTHONUNBUFFERED 1
ENV TZ=Asia/Seoul

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    libspdlog-dev \
    && rm -rf /var/lib/apt/lists/*

# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
#    && echo $TZ > /etc/timezone \
#    && apt-get update \
#    && apt-get install -y libspdlog-dev \
#    && pip install --upgrade pip \
#    && pip install -r requirements.txt --no-cache-dir \
#    && rm -rf /var/lib/apt/lists/* \
#    && rm -rf /var/cache/apt/archives \
#    && mkdir /app

RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir
COPY . /app/

EXPOSE 8000

RUN ["chmod", "+x", "./scripts/start.sh"]
CMD ["./scripts/start.sh"]