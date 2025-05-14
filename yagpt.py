import asyncio
import logging
import sys
import os

# Path to the 'yandexgpt-python-main' directory
# __file__ is /Users/kaycee/ChatGovorun/ChatGovorun/yagpt.py
# os.path.dirname(__file__) is /Users/kaycee/ChatGovorun/ChatGovorun
yandex_lib_parent_dir = os.path.dirname(os.path.abspath(__file__))
yandex_lib_dir_name = 'yandexgpt-python-main' # The actual directory name with hyphen
yandex_lib_path = os.path.join(yandex_lib_parent_dir, yandex_lib_dir_name)

# Add the directory containing 'yandex_gpt' module to sys.path
if yandex_lib_path not in sys.path:
    sys.path.insert(0, yandex_lib_path)

# Now, yandex_lib_path (e.g., .../ChatGovorun/yandexgpt-python-main) is in sys.path.
# We can import the 'yandex_gpt' package/module from inside it.
from yandex_gpt import YandexGPT, YandexGPTConfigManagerForAPIKey # Import from 'yandex_gpt' directly

class YandexGPTClient:
    def __init__(self, api_key, catalog_id):
        # Используем YandexGPTConfigManagerForAPIKey для конфигурации
        config = YandexGPTConfigManagerForAPIKey(
            model_type="yandexgpt", # или yandexgpt-lite, yandexgpt-pro
            catalog_id=catalog_id,
            api_key=api_key
        )
        self.client = YandexGPT(config_manager=config)
        
    async def get_response(self, message_text):
        logging.info(f"Entering get_response with message_text: '{message_text}'")
        try:
            # Формат сообщений для новой библиотеки
            messages = [{"role": "user", "text": message_text}]
            logging.info(f"Preparing to call YandexGPT with messages: {messages}")
            # Вызов нового метода для получения ответа
            completion = await self.client.get_async_completion(messages=messages)
            logging.info(f"Raw completion object from YandexGPT: {completion}") # Логируем сырой ответ
            # Извлечение текста ответа
            # Структура ответа может отличаться, нужно проверить документацию или примеры
            # Предполагаем, что ответ находится в completion.choices[0].message.text или аналогично
            # На основе README: print(completion) выводит объект, нужно посмотреть его структуру
            # Для примера из README, completion это строка, если модель возвращает простой текст
            # Если completion - это объект, нужно будет извлечь текст ответа.
            # Пока что, предположим, что completion это и есть текстовый ответ.
            # Если это объект, то, скорее всего, что-то вроде completion.result.alternatives[0].message.text
            # Уточним после теста или по более детальной документации SDK.
            # Судя по примеру из README: `print(completion)` выводит сам ответ.
            # Однако, в их коде `completion` это объект `CompletionResponse`.
            # `completion.result.alternatives[0].message.text` - это более вероятный путь.
            # Для простоты, пока оставим так, как будто completion это строка.
            # Если это не так, то нужно будет смотреть структуру объекта completion.
            # В README `completion` это объект, а не строка.
            # `completion.result.alternatives[0].message.text`
            # Давайте предположим, что `completion` это объект и нам нужен текст.
            # Если `get_async_completion` возвращает строку напрямую, то это будет работать.
            # Если это объект, то нужно будет адаптировать.
            # Судя по коду SDK (если заглянуть внутрь), get_async_completion возвращает строку.
            # logging.info(f"YandexGPT completion object: {completion}") # Уже залогировано выше как Raw completion object
            logging.info(f"YandexGPT completion type: {type(completion)}")
            # Попробуем извлечь текст ответа, предполагая, что completion - это объект
            try:
                if hasattr(completion, 'result') and completion.result and hasattr(completion.result, 'alternatives') and completion.result.alternatives:
                    response_text = completion.result.alternatives[0].message.text
                    logging.info(f"Extracted response text: {response_text}")
                    return response_text
                elif isinstance(completion, str):
                    logging.info("Completion is a string, returning directly.")
                    return completion
                else:
                    logging.warning("Unexpected completion object structure. Returning raw completion.")
                    return str(completion) # Возвращаем строковое представление, если структура неизвестна
            except AttributeError as ae:
                logging.error(f"AttributeError while accessing completion parts: {ae}. Completion object: {completion}")
                # Если это строка, вернем ее. Иначе, проблема.
                if isinstance(completion, str):
                    return completion
                return "Ошибка извлечения текста из ответа YandexGPT."
            except Exception as ex:
                logging.error(f"Unexpected error while processing completion: {ex}. Completion object: {completion}")
                return "Неожиданная ошибка при обработке ответа YandexGPT."
        except Exception as e:
            logging.error(f"Ошибка при вызове или первоначальной обработке ответа от YandexGPT: {e}", exc_info=True)
            return "Произошла ошибка при обработке вашего запроса к YandexGPT."