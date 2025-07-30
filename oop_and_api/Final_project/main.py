import os
import logging
from dotenv import load_dotenv
from logging_config import setup_logging
from api_vk import ApiVK
from api_yd import ApiYd

# Загружаем переменные из .env
load_dotenv()

# Получаем токены из переменных окружения
vk_api_key = os.getenv('API_KEY_VK')
yd_api_key = os.getenv('TOKEN_YD')

# Настройка логирования
setup_logging()


def loader_from_vk_to_yadisk(vk_token, yd_token, user_id, count):
    try:
        logging.info("Начало загрузки данных из VK на Яндекс.Диск.")

        # Инициализация API VK
        vk = ApiVK(vk_token)
        logging.info(f"Запрос фотографий пользователя {user_id} из VK (количество: {count}).")

        # Получение фотографий из VK
        response = vk.get_photos(user_id, count)
        if not response:
            logging.error("Не удалось получить фотографии из VK.")
            return

        # Создание JSON-файла с информацией о фотографиях
        data = vk.make_json(response)
        logging.info(f"Создан JSON-файл с информацией о {len(data)} фотографиях.")

        # Сохранение фотографий локально
        vk.save_photos_locally(data)
        logging.info("Фотографии успешно сохранены локально.")

        # Инициализация API Яндекс.Диска
        yadisk = ApiYd(yd_token)
        logging.info(f"Создание папки для пользователя {user_id} на Яндекс.Диске.")

        # Создание папки на Яндекс.Диске
        yadisk.create_new_folder(user_id)

        # Загрузка фотографий на Яндекс.Диск
        logging.info(f"Начало загрузки {len(data)} фотографий на Яндекс.Диск.")
        yadisk.load_photo('vk_photos', user_id)

        logging.info("Все фотографии успешно загружены на Яндекс.Диск.")

    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    loader_from_vk_to_yadisk(vk_api_key, yd_api_key, '52112515', 5)