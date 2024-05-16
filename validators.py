import logging
import math
from config import LOGS, maxusers, max_user_gpt_tokens, max_user_stt_blocks, max_user_tts_symbols, admins_ids
from database import count_users, count_all_limits
from gpt import count_gpt_tokens

logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")


def check_number_of_users(user_id):
    count = count_users(user_id)
    if count is None:
        return None, "Ошибка при работе с БД"
    if count > maxusers:
        return None, "Превышено максимальное количество пользователей"
    return True, ""


def is_gpt_token_limit(messages, total_spent_tokens, user_id):
    all_tokens = count_gpt_tokens(messages) + total_spent_tokens
    if all_tokens > max_user_gpt_tokens and str(user_id) not in admins_ids:
        return None, f"Превышен общий лимит GPT-токенов {max_user_gpt_tokens}"
    return all_tokens, ""


def is_stt_block_limit(user_id, duration):
    audio_blocks = math.ceil(duration / 15)
    all_blocks = count_all_limits(user_id, 'stt_blocks') + audio_blocks

    if duration >= 30:
        response = "SpeechKit STT работает с голосовыми сообщениями меньше 30 секунд"
        return None, response

    if all_blocks >= max_user_stt_blocks and str(user_id) not in admins_ids:
        response = (f"Превышен общий лимит SpeechKit STT {max_user_stt_blocks}. Использовано {all_blocks} блоков. "
                    f"Доступно: "f"{max_user_stt_blocks - all_blocks}")
        return None, response

    return audio_blocks, None


def is_tts_symbol_limit(user_id, text):
    text_symbols = len(text)

    all_symbols = count_all_limits(user_id, 'tts_symbols') + text_symbols

    if all_symbols >= max_user_tts_symbols and str(user_id) not in admins_ids:
        msg = (f"Превышен общий лимит SpeechKit TTS {max_user_tts_symbols}. Использовано: {all_symbols} символов. "
               f"Доступно: {max_user_tts_symbols - all_symbols}")
        return None, msg

    return text_symbols, None
