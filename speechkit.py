import requests
import logging
from config import iam, LOGS, folder_id

logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")


def text_to_speech(text):
    headers = {
        'Authorization': f'Bearer {iam}',
    }
    data = {
        'text': text,
        'lang': 'ru-RU',
        'voice': 'filipp',
        'folderId': folder_id
    }
    response = requests.post(
        'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
        headers=headers,
        data=data
    )
    if response.status_code == 200:
        return True, response.content
    else:
        return False, response


def speech_to_text(data):
    params = "&".join([
        "topic=general",
        f"folderId={folder_id}",
        "lang=ru-RU"
    ])

    headers = {
        'Authorization': f'Bearer {iam}',
    }

    response = requests.post(
        "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?"+params,
        headers=headers,
        data=data
    )

    decoded_data = response.json()

    if decoded_data.get("error_code") is None:
        logging.info('Получен ответ от нейросети')
        return True, decoded_data.get("result")

    else:
        msg = "При запросе в SpeechKit возникла ошибка"
        logging.error(msg)
        return False, msg
