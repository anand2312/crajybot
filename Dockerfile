FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get -y update \
    && apt-get install -y \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /bot

COPY pyproject.toml ./
COPY poetry.lock ./

RUN pip install -U poetry

RUN poetry install

COPY . .

CMD ["poetry", "run", "python", "bot.py"]