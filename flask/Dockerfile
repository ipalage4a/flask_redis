FROM python:3.7
WORKDIR /app
RUN pip install flask flask-restful flask-redis
ENV REDIS_URL redis://:password@localhost:6379/0
