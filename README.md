# Crajy Bot
A Discord Bot.

## Requirements
- Python >= 3.8
- Poetry

## Setting up
- Run `poetry install` to install dependencies
- Run `prisma db push` to create the SQLite database
- Add constants:
    - add the bot token as a constant named `TOKEN` in `secret/TOKEN.py`
    - add the ID of the testing server as a constant named `BOT_TEST_SERVER` in `secret/constants.py`
    - add the ID of the testing channel as a constant named `BOT_TEST_CHANNEL` in `secret/constants.py`

## Running
`python manage.py` -> Runs the bot and attempts to load all extensions
`python manage.py --exts ext1 ext2 ext3` -> Runs the bot and only loads `ext1`, `ext2`, `ext3`
