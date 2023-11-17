from time import time, sleep

import requests
import telegram
from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

auth_token = env.str("AUTHORIZATION_TOKEN")
telegram_chat_id = env.str("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=env.str("TELEGRAM_TOKEN"))

url = "https://dvmn.org/api/long_polling/"
headers = {"Authorization": f"Token {auth_token}"}
params = {"timestamp": time()}

while True:
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        json_respone_data = response.json()

        if json_respone_data["status"] == "found":
            new_attempts = json_respone_data["new_attempts"][0]
            text = f'You have checked the work of "{new_attempts["lesson_title"]}"!\n\n'
            if new_attempts["is_negative"]:
                text += "Unfortunately, there were errors in the work!\n"
            else:
                text += "The teacher liked everything, you can proceed to the next lesson!\n"
            text += f'Go to the lesson to see {new_attempts["lesson_url"]}'
            bot.send_message(chat_id=telegram_chat_id, text=text)
        elif json_respone_data["status"] == "timeout":
            params = {"timestamp": json_respone_data["timestamp_to_request"]}

    except requests.exceptions.ReadTimeout:
        print("Time occurred!")
    except requests.exceptions.ConnectionError:
        sleep(5)
        print("No internet connection!")
        continue
