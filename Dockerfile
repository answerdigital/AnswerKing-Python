# syntax=docker/dockerfile:1

FROM python:3.10.8-buster

RUN pip install poetry
COPY . /AnswerKing-Python
WORKDIR /AnswerKing-Python
#ENV PATH="${PATH}:/root/.local/bin"
RUN poetry install --only main

CMD [ "/usr/local/bin/poetry", "run", "python", "manage.py", "migrate", "0.0.0.0:8000"]
CMD [ "/usr/local/bin/poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
EXPOSE 8000
