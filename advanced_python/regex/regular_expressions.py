from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)

"""
Ваша задача:

1. Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно.
В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О.
Подсказка: работайте со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" "), регулярки здесь НЕ НУЖНЫ.
2. Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999.
Подсказка: используйте регулярки для обработки телефонов.
3. Объединить все дублирующиеся записи о человеке в одну.
Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).
"""

# TODO 1: выполните пункты 1-3 ДЗ

def split_fullname(fullname):
  parts = fullname.strip().split()
  if len(parts) == 3:
    return parts
  elif len(parts) == 2:
    return parts[0], parts[1], ''
  elif len(parts) == 1:
    return parts[0], '', ''
  else:
    return '', '', ''

def normalize_phone(phone):
    phone = re.sub(r'\D', '', phone)
    if not phone:
      return ''

    if phone.startswith('8'):
      phone = '+7' + phone[1:]

    if len(phone) >= 11:
      main = phone[:11]
      formatted = f"+7({main[1:4]}){main[4:7]}-{main[7:9]}-{main[9:11]}"
      if len(phone) > 11:
        formatted += f" доб.{phone[11:]}"
      return formatted
    else:
      return phone


processed = {}

for contact in contacts_list[1:]:
  raw_fullname = ' '.join(contact[:3]).strip()
  lastname, firstname, surname = split_fullname(raw_fullname)
  full_name_key = f"{lastname} {firstname}".strip()

  # Нормализация данных
  phone = normalize_phone(contact[5])
  email = contact[6].strip()
  organization = contact[3].strip()
  position = contact[4].strip()

  # Если ключа ещё нет в словаре — создаём шаблон
  if full_name_key not in processed:
    processed[full_name_key] = {
      'lastname': '',
      'firstname': '',
      'surname': '',
      'organization': '',
      'position': '',
      'phone': '',
      'email': ''
    }

  target = processed[full_name_key]

  # Обновляем только если значение не пустое
  target['lastname'] = target['lastname'] or lastname
  target['firstname'] = target['firstname'] or firstname
  target['surname'] = target['surname'] or surname
  target['organization'] = target['organization'] or organization
  target['position'] = target['position'] or position
  target['phone'] = target['phone'] or phone
  if email:
    target['email'] = email


final_data = [contacts_list[0]]
for key, info in processed.items():
    final_data.append([
        info['lastname'],
        info['firstname'],
        info['surname'],
        info['organization'],
        info['position'],
        info['phone'],
        info['email']
    ])

# Вывод результата
pprint(final_data)



# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(final_data)