# Work Notifier Bot

## Description

Telegram bot to receive notifications about checking work on [Devman](https://dvmn.org/).

## How to install?

Python3 should be already installed. 
Then use `pip` (or `pip3` for Python3) to install dependencies:

```commandline
pip install -r requirements.txt
```

Recommended using [virtualenv/venv](https://docs.python.org/3/library/venv.html)

## Environment variables

Some of the project settings come from environment variables. To define them, create a `.env` file and write the data there in this format: `VARIABLE=value`.

There are 3 variables available:
- `AUTHORIZATION_TOKEN` — Devman authorization token to work with the API 
- `TELEGRAM_TOKEN` — Telegram token to work with the API
- `TELEGRAM_CHAT_ID` - ID of telegram chat. It can be obtained by sending a message to the @userinfobot bot

## Launch

Run the script by the following command:

```sh
python main.py
```