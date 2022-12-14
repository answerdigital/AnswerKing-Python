# syntax=docker/dockerfile:1

FROM python:3.10.8-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /AnswerKing-Python
WORKDIR /AnswerKing-Python

RUN pip install poetry
RUN poetry install --only main
RUN pip install make

CMD [ "/usr/bin/make", "dockerRunserver"]
