FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

WORKDIR /bot

COPY pyproject.toml ./
COPY poetry.lock ./

RUN pip install -U poetry

RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "bot.py"]