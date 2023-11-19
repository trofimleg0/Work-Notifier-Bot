from time import time, sleep

import requests
import telegram
from environs import Env


def main():
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
            checking_result = response.json()

            if checking_result["status"] == "found":
                new_attempts = checking_result["new_attempts"][0]
                text = f'You have checked the work of "{new_attempts["lesson_title"]}"!\n\n'
                if new_attempts["is_negative"]:
                    text += "Unfortunately, there were errors in the work!\n"
                else:
                    text += "The teacher liked everything, you can proceed to the next lesson!\n"
                text += f'Go to the lesson to see {new_attempts["lesson_url"]}'
                bot.send_message(chat_id=telegram_chat_id, text=text)
            elif checking_result["status"] == "timeout":
                params = {"timestamp": checking_result["timestamp_to_request"]}

        except requests.exceptions.HTTPError:
            continue
        except requests.exceptions.ConnectionError:
            sleep(5)
            continue


if __name__ == "__main__":
    main()
