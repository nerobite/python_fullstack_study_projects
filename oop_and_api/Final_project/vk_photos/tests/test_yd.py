import pytest

from oop_and_api.Final_project.api_yd import ApiYd

@pytest.fixture
def api():
    return ApiYd('fake_token')


def test_create_new_folder_success(api, requests_mock):
    # Мокаем ответ: успешное создание папки
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    requests_mock.put(url, status_code=201)

    # Вызов
    api.create_new_folder('test_folder')

    # Проверим, что запрос был сделан
    assert requests_mock.called
    # Проверим, что был вызван ровно один раз
    assert requests_mock.call_count == 1
    # Проверим, что URL и параметры правильные
    request = requests_mock.request_history[0]
    assert request.method == 'PUT'
    assert request.qs['path'] == ['/test_folder']  # qs — query string в виде словаря


def test_create_new_folder_already_exists(api, requests_mock):
    # Мокаем ответ: папка уже существует
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    requests_mock.put(url, status_code=409)

    api.create_new_folder('existing_folder')

    assert requests_mock.called
    request = requests_mock.request_history[0]
    assert request.qs['path'] == ['/existing_folder']


def test_create_new_folder_server_error(api, requests_mock):
    # Мокаем ответ: внутренняя ошибка сервера
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    requests_mock.put(url, status_code=500, json={'message': 'Internal Server Error'})

    api.create_new_folder('error_folder')

    assert requests_mock.called
    request = requests_mock.request_history[0]
    assert request.qs['path'] == ['/error_folder']
