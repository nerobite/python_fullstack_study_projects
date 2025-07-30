import requests
import os
import logging
from dotenv import load_dotenv
from urllib.parse import urljoin
from logging_config import setup_logging

# Загружаем переменные окружения
load_dotenv()

# Получаем токен из .env
yd_api_key = os.getenv('TOKEN_YD')

# Настройка логирования
setup_logging()


class ApiYd:
    def __init__(self, yd_api_key):
        self.yd_api_key = yd_api_key
        self.base_url = 'https://cloud-api.yandex.net'
        self.headers = {
            'Authorization': f'OAuth {self.yd_api_key}'
        }
        self.folder_url = urljoin(self.base_url, '/v1/disk/resources')

    def create_new_folder(self, folder_name):
        params = {'path': f'/{folder_name.lstrip("/")}'}
        response = requests.put(self.folder_url, headers=self.headers, params=params)
        if response.status_code == 201:
            logging.info(f'Папка "{folder_name}" успешно создана.')
        elif response.status_code == 409:
            logging.warning(f'Папка "{folder_name}" уже существует.')
        else:
            logging.error(f'Ошибка при создании папки: {response.status_code}, {response.json()}')

    def load_photo(self, local_folder, yd_folder):
        if not os.path.exists(local_folder):
            logging.error(f'Папка {local_folder} не найдена.')
            return

        upload_url = urljoin(self.base_url, '/v1/disk/resources/upload')
        yd_folder = f'/{yd_folder.lstrip("/")}'

        for filename in os.listdir(local_folder):
            local_path = os.path.join(local_folder, filename)
            if os.path.isfile(local_path):
                yd_path = f'{yd_folder}/{filename}'

                # Формируем параметры для текущего запроса
                params = {
                    'path': yd_path,
                    'overwrite': 'true'
                }
                response = requests.get(upload_url, headers=self.headers, params=params)  # Используем GET для /upload
                logging.info(f'Статус для {filename}: {response.status_code}')
                if response.status_code == 200:
                    href = response.json().get('href')
                    with open(local_path, 'rb') as f:
                        upload_response = requests.put(href, data=f)  # Загружаем файл
                    if upload_response.status_code == 201:
                        logging.info(f'Файл "{filename}" успешно загружен.')
                    else:
                        logging.error(f'Ошибка при загрузке "{filename}": {upload_response.status_code}, {upload_response.json()}')
                else:
                    logging.error(f'Не удалось получить upload URL для {filename}: {response.status_code}, {response.json()}')

    def delete_folder(self, folder_name):
        params = {'path': f'/{folder_name.lstrip("/")}'}
        response = requests.delete(self.folder_url, headers=self.headers, params=params)
        if response.status_code == 204:  # Код 204 означает успешное удаление без содержимого в ответе
            logging.info(f'Папка "{folder_name}" успешно удалена.')
        elif response.status_code == 404:
            logging.warning(f'Папка "{folder_name}" не найдена.')
        else:
            logging.error(f'Ошибка при удалении папки: {response.status_code}, {response.text}')


if __name__ == '__main__':
    yam = ApiYd(yd_api_key)
    # yam.create_new_folder('52112515')
    # responce = yam.load_photo('vk_photos', '52112515')
    # print(responce)
    yam.delete_folder('52112515')
