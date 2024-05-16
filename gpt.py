import json

import requests
import logging
from config import LOGS, max_gpt_tokens, SYSTEM_PROMPT, iam, folder_id, tokenize_url, gptmodel, url_gpt


logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")


def count_gpt_tokens(messages):
    headers = {
        'Authorization': f'Bearer {iam}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/yandexgpt-lite",
        "messages": messages
    }
    try:
        response = requests.post(url=tokenize_url, json=data, headers=headers).json()['tokens']
        return len(response)
    except Exception as e:
        logging.error(e)
        return 0


def ask_gpt(messages):
    headers = {
        'Authorization': f'Bearer {iam}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{folder_id}/{gptmodel}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": max_gpt_tokens
        },
        "messages": SYSTEM_PROMPT + messages
    }
    try:
        response = requests.post(url_gpt, headers=headers, json=data)
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)
        return False, "Не удалось подключиться к GPT",  None


if __name__ == '__main__':
    print(count_gpt_tokens([{'role': 'user', 'text': 'Привет'}]))
