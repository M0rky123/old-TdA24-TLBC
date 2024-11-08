# syntax=docker/dockerfile:1

FROM python:3.10-buster

WORKDIR /app

RUN pip install pipenv flask[async] requests

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --system --deploy

COPY . .

EXPOSE 80

CMD ["./start.sh"]

