import pytest
import requests
from oop_and_api.Project_4 import get_the_smartest_superhero, get_the_smartest_superhero_ids

def test_get_the_smartest_superhero(requests_mock):
    # Подменяем URL
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    mock_data = [
        {'name': 'Hulk', 'powerstats': {'intelligence': 80}},
        {'name': 'Captain America', 'powerstats': {'intelligence': 90}},
        {'name': 'Thanos', 'powerstats': {'intelligence': 95}}
    ]
    requests_mock.get(url, json=mock_data)

    result = get_the_smartest_superhero()
    assert result == 'Thanos'


def test_get_the_smartest_superhero_ids(requests_mock):
    # Подменяем URL
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    mock_data = [
        {'id': 1, 'name': 'Hulk', 'powerstats': {'intelligence': 80}},
        {'id': 2, 'name': 'Captain America', 'powerstats': {'intelligence': 90}},
        {'id': 3, 'name': 'Thanos', 'powerstats': {'intelligence': 95}},
        {'id': 4, 'name': 'Batman', 'powerstats': {'intelligence': 100}}
    ]
    requests_mock.get(url, json=mock_data)

    result = get_the_smartest_superhero_ids([1,2,3,4])
    assert result == 'Batman'


def test_superhero_api_connection():
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)

    # Проверяем статус-код
    assert response.status_code == 200

    # Проверяем, что ответ — JSON список
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Проверим, что у первого героя есть ключ name и powerstats
    first = data[0]
    assert 'name' in first
    assert 'powerstats' in first
