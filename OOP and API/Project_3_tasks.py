import json
import xml.etree.ElementTree as ET

"""
Задача №1
Вам дан json-файл с новостями. Написать программу, которая будет выводить топ 10 самых часто встречающихся в новостях
слов длиннее 6 символов.
Приведение к нижнему регистру не требуется.
В результате корректного выполнения задания будет выведен следующий результат:
['туристов', 'компании', 'Wilderness', 'странах', 'туризма', 'которые', 'африканских', 'туристы', 'является', 'природы']
"""

file_path = 'Project_3_data/newsafr.json'

def read_json(file_path, word_max_len=6, top_words_amt=10):
    """
    функция для чтения файла с новостями.
    """
    string_words = []
    count_words = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        loaded_data = json.load(f)
        for line in loaded_data['rss']['channel']['items']:
            str_words = line['description'].strip().split()
            string_words.extend([word for word in str_words if len(word) > word_max_len])
    for word in string_words:
        count_words[word] = count_words.get(word, 0) +1
    sorted_words = sorted(count_words.items(), key = lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:top_words_amt]]

if __name__ == '__main__':
    print(read_json(file_path))


"""
Задача №2
Вам дан xml-файл с новостями. Написать программу, которая будет выводить топ 10 самых часто встречающихся в новостях
слов длиннее 6 символов.
Приведение к нижнему регистру не требуется.
В результате корректного выполнения задания будет выведен следующий результат:
['туристов', 'компании', 'Wilderness', 'странах', 'туризма', 'которые', 'африканских', 'туристы', 'является', 'природы']
"""

file_path = 'Project_3_data/newsafr.xml'

def read_xml(file_path, word_max_len=6, top_words_amt=10):
    """
    функция для чтения файла с новостями.
    """
    string_words = []
    count_words = {}
    parser = ET.XMLParser(encoding = "utf-8")
    tree = ET.parse(file_path, parser)
    root = tree.getroot()
    news_list = root.findall("channel/item")
    for news in news_list:
        description = news.find("description")
        string_words.extend(description.text.strip().split())
    for word in string_words:
        count_words[word] = count_words.get(word, 0) +1
    sorted_words = sorted(count_words.items(), key = lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words if len(word) > word_max_len][:top_words_amt]



if __name__ == '__main__':
    print(read_xml(file_path))