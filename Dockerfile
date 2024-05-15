FROM python:3.11-slim
MAINTAINER Daniel Lassahn <daniel.lassahn@meteointelligence.de>

RUN apt-get update && apt-get install -y gcc g++ build-essential

COPY ./requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt


COPY .env .env
ENV PYTHONPATH "/:/app"
WORKDIR /app
COPY entrypoint.sh /
COPY . .

ENTRYPOINT ["/entrypoint.sh"]