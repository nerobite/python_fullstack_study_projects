import requests
import os
import json
import logging
from urllib.parse import urljoin
from dotenv import load_dotenv
from logging_config import setup_logging

# Загружаем переменные из .env
load_dotenv()

# Настройка логирования
setup_logging()

vk_api_key =  os.getenv('API_KEY_VK')


class ApiVK:
    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }
        self.base = 'https://api.vk.com/method/'
        logging.info("Инициализация класса ApiVK завершена.")

    def get_friends(self, user_id, count=5):
        # Формируем URL с помощью urljoin
        endpoint = 'friends.get'
        url = urljoin(self.base, endpoint)
        params = {
            'user_id': user_id,
            'count': count,
            'fields': 'bdate'
        }
        params.update(self.params)
        logging.info(f"Запрос списка друзей для user_id={user_id}, количество={count}.")
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logging.info(f"Список друзей успешно получен.")
        else:
            logging.error(f"Ошибка при получении списка друзей: {response.status_code}, {response.text}")
        return response.json()

    def get_photos(self, user_id, count=10):
        # Формируем URL с помощью urljoin
        endpoint = 'photos.get'
        url = urljoin(self.base, endpoint)
        params = {
            'owner_id': user_id,
            'count': count,
            'album_id': 'profile',
            'extended': 1
        }
        params.update(self.params)
        logging.info(f"Запрос фотографий для user_id={user_id}, количество={count}.")

        try:
            response = requests.get(url, params=params)

            # Логируем статус ответа
            if response.status_code == 200:
                logging.info("Фотографии успешно получены.")
            else:
                logging.error(f"Ошибка при получении фотографий: {response.status_code}, {response.text}")
                raise Exception(f"Ошибка API: {response.status_code}, {response.text}")

            # Пытаемся разобрать JSON только при успешном статусе
            data = response.json()

            # Проверяем структуру ответа
            info = data.get('response', {}).get('items', [])
            if not info:
                logging.warning("Ответ не содержит фотографий.")

            return info
        except requests.exceptions.RequestException as e:
            # Обработка ошибок сети (например, timeout, connection error)
            logging.error(f"Сетевая ошибка: {e}")
            raise Exception(f"Сетевая ошибка: {e}")

        except ValueError as e:
            # Обработка ошибок при парсинге JSON
            logging.error(f"Ошибка при разборе JSON: {e}")
            raise Exception(f"Ошибка при разборе JSON: {e}")

    def create_name(self, item):
        name = []
        name_info = item.get('likes', {}).get('count', {})
        if name_info not in name:
            name.append(f'{str(name_info)}.jpg')
        else:
            name_info = name_info + item.get('date', {})
            name.append(f'{str(name_info)}.jpg')
        logging.info(f"Создано имя файла: {name[0]}")
        return name[0]

    def get_largest_photo(self, sizes):
        priority = {'s': 1, 'm': 2, 'x': 3, 'y': 4, 'z': 5, 'o': 6}
        max_priority = 0
        max_url = None
        max_type = None

        for size in sizes:
            p = priority.get(size['type'], 0)
            if p > max_priority:
                max_priority = p
                max_url = size['url']
                max_type = size['type']

        logging.info(f"Выбрана фотография с максимальным размером: type={max_type}, url={max_url}")
        return max_type, max_url

    def max_size_photo(self, item):
        # Проверка на наличие оригинального фото
        orig_photo = item.get('orig_photo')
        if isinstance(orig_photo, dict) and 'type' in orig_photo and 'url' in orig_photo:
            logging.info(f"Найдено оригинальное фото: type={orig_photo['type']}, url={orig_photo['url']}")
            return orig_photo['type'], orig_photo['url']

        # Получаем список размеров
        sizes = item.get('sizes', [])
        if not sizes:
            logging.warning("Не найдены доступные размеры фото.")
            return None, None
        return self.get_largest_photo(sizes)

    def make_json(self, info):
        data = []
        for item in info:
            file_name = self.create_name(item)
            best_size, best_type_url = self.max_size_photo(item)
            data.append(
                {
                    'file_name': file_name,
                    'size': best_size,
                    'url': best_type_url
                })
        with open('info.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info("Данные успешно сохранены в файл info.json.")
        return data

    def save_photos_locally(self, data, folder='vk_photos'):
        if not os.path.exists(folder):
            os.makedirs(folder)
            logging.info(f"Создана папка: {folder}")

        for item in data:
            file_name = item['file_name']
            url = item['url']
            path = os.path.join(folder, file_name)

            response = requests.get(url)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(response.content)
                logging.info(f"Файл {file_name} успешно сохранен локально.")
            else:
                logging.error(f"Ошибка при загрузке файла {file_name}: {response.status_code}, {response.text}")



#52112515
if __name__ == '__main__':
    vk = ApiVK(vk_api_key)
    response = vk.get_photos(52112515, 5)
    #response = vk.create_name(response)
    data = vk.make_json(response)
    vk.save_photos_locally(data)

