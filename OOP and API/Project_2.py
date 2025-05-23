from pprint import pprint
import os
import json

# Задача №1
cook_book = {}
with open("Project_2_data/recipes.txt", encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if "|" not in line and not line.isdigit():
            dish = line.lower()
            cook_book[dish] = []
        if "|" in line:
            ingredients = [i.strip() for i in line.split("|")]
            if len(ingredients) != 3:
                print(f"Ошибка в строке: {line}")
                continue
            cook_book[dish].append({'ingredient_name': ingredients[0], 'quantity': int(ingredients[1]), \
                                    'measure': ingredients[2]})
#pprint(cook_book)

with open("Project_2_data/cook_book.json", "w", encoding="utf-8") as f:
    json.dump(cook_book, f, ensure_ascii=False, indent=4)



# Задача №2
def get_shop_list_by_dishes(dishes, person_count, cook_book):
    res = {}
    for dish in dishes:
        dish = dish.lower()
        if dish in cook_book:
            for item in cook_book[dish]:
                name = item['ingredient_name']
                qty = item['quantity'] * person_count
                if name in res:
                    res[name]['quantity'] += qty
                else:
                    res[name] = {'quantity': qty, 'measure': item['measure']}
        else:
            print(f'Блюдо "{dish}" не найдено.')
    return res

dish_list = get_shop_list_by_dishes(['Запеченный картофель', 'Омлет', 'Фахитос'], 2, cook_book)
#pprint(dish_list)

with open("Project_2_data/dish_list.json", "w", encoding="utf-8") as f:
    json.dump(dish_list, f, ensure_ascii=False, indent=4)


#Задача №3
data_files = ['Project_2_data/1.txt',
              'Project_2_data/2.txt',
              'Project_2_data/3.txt']
string_data = {}
for path in data_files:
    file_name = os.path.splitext(os.path.basename(path))
    name = file_name[0] + file_name[1]
    with open(path, encoding='utf-8') as f:
        for n, line in enumerate(f, start=1):
            string_data.setdefault(name, []).append(f'Строка номер {n} файла номер {file_name[0]}')
            string_data.setdefault(name, []).append(line.strip())

#print(string_data)

sorted_data = dict(sorted(string_data.items(), key=lambda x: len(x[1]) // 2))
data = ''
for key, text in sorted_data.items():
    data += key + '\n'
    data += str(len(text) // 2) + '\n'
    data += '\n'.join(text) + '\n'

# print(data)
with open("Project_2_data/data.txt", "w", encoding="utf-8") as f:
    f.write(data)

