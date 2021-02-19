FROM python:3.8-slim

RUN apt-get -y update \
    && apt-get install -y \
        git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /bot

COPY poetry.lock ./

RUN pip install -U poetry

RUN poetry install

COPY . .

ENTRYPOINT ["python3"]

CMD ["bot.py"]