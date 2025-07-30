import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()

"""
Есть API по информации о супергероях с информацией по всем супергероям.
https://akabab.github.io/superhero-api/api/
Напишите функцию для определения самого умного супергероя среди Hulk, Captain America, Thanos.
"""
def get_the_smartest_superhero() -> str:
    the_smartest_superhero = ''
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)
    intelect = 0
    for data_list in response.json():
        if data_list['name'] in ['Hulk', 'Captain America', 'Thanos']:
            if intelect < data_list['powerstats']['intelligence']:
                intelect = data_list['powerstats']['intelligence']
                the_smartest_superhero = data_list['name']
    return the_smartest_superhero

print(f'Самый умный супергерой - {get_the_smartest_superhero()}')

"""
Есть API по информации о супергероях с информацией по всем супергероям.
Теперь нужно найти самого умного супергероя среди списка супергероев.
Напишите функцию get_the_smartest_superhero, которая принимает на вход список superheros, состоящий из id.
"""
def get_the_smartest_superhero_ids(superheros):
    the_smartest_superhero = ''
    url = 'https://akabab.github.io/superhero-api/api/all.json'
    response = requests.get(url)
    intelect = 0
    for data_list in response.json():
        if data_list['id'] in superheros:
            if intelect < data_list['powerstats']['intelligence']:
                intelect = data_list['powerstats']['intelligence']
                the_smartest_superhero = data_list['name']
    return the_smartest_superhero

print(f'Самый умный супергерой из списка - {get_the_smartest_superhero_ids([1, 2, 3, 4, 5])}')

"""
У Яндекса есть очень удобное API для словарей(https://yandex.ru/dev/dictionary/).
Там можно переводить слова с одного языка на другой.
Ваша задача – написать функцию, которая принимает русское слово и возвращает его перевод на английском языке.
Для работы с API вам потребуется получить токен(https://yandex.ru/dev/dictionary/keys/get/?service=dict).
В описании введите «Для обучения» и вы получите бесплатный токен.
"""
token = os.getenv('TOKEN')
url = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

def translate_word(word):
    params = {
        'key': token,
        'lang': 'ru-en',
        'text': word
    }
    response = requests.get(url, params=params)
    return response.json()['def'][0]['tr'][0]['text']

print(f'Получено слово {"питон"} перевод {translate_word("питон")}')

"""
Альберт Эйнштейн, возвращаясь из своей очередной научной конференции, решил разыграть свою жену. Он ей рассказал,
что посетил большое количество европейских городов, но больше всего ему понравился город из Великобритании.
И пообещал ей, если она сможет найти по координатам этот город, то свозит её туда в ближайший отпуск.
Целую неделю Эльза работала с картами, чтобы найти нужный город. А как мы были решили эту задачу, имея API и интернет?

Напишите функцию, которая принимает на вход список из координат (кортеж из широты и долготы)
и возращает английский город. Список городов Великобритании ограничен 8 самыми популярными городами: Leeds, London,
Liverpool, Manchester, Oxford, Edinburgh, Norwich, York. Гарантируется,
что в списке есть как минимум 1 британский город.
Для нахождения города по координатам рекомендуется использовать API geocode(https://geocode.maps.co/).
"""


coordinates = [
    ('55.7514952', '37.618153095505875'),
    ('52.3727598', '4.8936041'),
    ('53.4071991', '-2.99168')
]

def find_uk_city(coordinates:list) -> str:
    url = 'https://geocode.maps.co/reverse'
    api_key = os.getenv('API_KEY')
    uk_list = ['Leeds', 'London', 'Liverpool', 'Manchester',
                            'Oxford', 'Edinburgh', 'Norwich', 'York']
    for lat, lon in coordinates:
        params = {
            'api_key': api_key,
            'lat': lat,
            'lon': lon
        }
        response = requests.get(url, params=params)
        city = response.json()['address']['city']
        time.sleep(0.1)
        if city in uk_list:
            return city

print(f'Город который понравился Эйнштейну - {find_uk_city(coordinates)}')